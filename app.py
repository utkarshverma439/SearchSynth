import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import asyncio
import aiohttp
import re
import time

# Google Sheets and authentication setup
scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

st.title("SearchSynth")

# Step 1: Upload CSV or Connect Google Sheet
st.header("Upload CSV or Connect Google Sheet")

# File upload for CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Google Sheets URL input
sheet_url = st.text_input("Enter Google Sheet URL:")

def get_spreadsheet_id(url):
    """Extracts spreadsheet ID from a Google Sheets URL."""
    try:
        return url.split("/d/")[1].split("/")[0]
    except Exception as e:
        st.error(f"Error extracting spreadsheet ID: {e}")
        return None

def fetch_data_from_sheet(spreadsheet_id):
    """Fetches data from a Google Sheet using its ID."""
    try:
        workbook = client.open_by_key(spreadsheet_id)
        sheet = workbook.sheet1
        data = sheet.get_all_values()
        return pd.DataFrame(data[1:], columns=data[0])  # Skip header row
    except Exception as e:
        st.error(f"Error fetching data from Google Sheets: {e}")
        return None

# Handling CSV file upload
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data", data.head())
    df = data  # Store the uploaded data in df

# Handling Google Sheets connection
if st.button("Connect to Google Sheets") and sheet_url:
    # Extract the spreadsheet ID from the URL
    spreadsheet_id = get_spreadsheet_id(sheet_url)

    if spreadsheet_id:
        # Fetch the data from the sheet and display it
        df = fetch_data_from_sheet(spreadsheet_id)
        if df is not None:
            st.write("Data from Google Sheet:")
            st.dataframe(df)
    else:
        st.error("Invalid Google Sheets URL. Please check the URL format.")

# Column selector and display
if uploaded_file is not None or sheet_url:
    if 'df' in locals():  # Check if 'df' (DataFrame) is defined
        # Display a dropdown to select the main column
        main_column = st.selectbox("Select the main column", df.columns)

        # Display the selected column's data
        st.write(f"Data from the selected column: {main_column}")
        st.write(df[main_column])

# Step 2: Dynamic Query Input
st.header("Define Your Search Query")
query_template = st.text_input("Enter the search query template")

# Step 3: Integrate with SerpApi
API_KEY = st.secrets["api_keys"]["serpapi_api_key"]
BASE_URL = 'https://serpapi.com/search'

async def fetch_results(session, query, start_index=0, num_results=10):
    params = {
        'q': query,
        'api_key': API_KEY,
        'num': num_results,
        'start': start_index
    }
    async with session.get(BASE_URL, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            return None

async def scrape_and_summarize(query, num_pages=1, results_per_page=10):
    tasks = []
    summaries = []
    async with aiohttp.ClientSession() as session:
        for page in range(num_pages):
            start_index = page * results_per_page
            task = fetch_results(session, query, start_index, results_per_page)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)

        # Process and summarize each result
        for result in results:
            if result and 'organic_results' in result:
                count = 0
                for item in result['organic_results']:
                    if count >= 3:  # Limit to top 3 results
                        break
                    title = item.get('title', 'No title')
                    link = item.get('link', 'No link')
                    snippet = item.get('snippet', 'No snippet')
                    summary = f"**{count+1}. {title}**<br> [{title}]({link}) - {snippet}"
                    summaries.append(summary)
                    count += 1
            time.sleep(1)  # Respect rate limits (optional, adjust as needed)
    
    return summaries

async def update_csv_with_summaries_and_groq(df, column_name, num_pages=1, results_per_page=10):
    """Fetch, summarize, and pass data to Groq in one go."""
    
    if column_name not in df.columns:
        st.error(f"Column '{column_name}' not found in CSV.")
        return
    
    # Process each row, fetch and summarize the data from SerpApi
    for index, row in df.iterrows():
        query = row[column_name]
        st.write(f"Fetching results for: {query}")
        
        # Fetch and summarize results from SerpApi
        summaries = await scrape_and_summarize(query, num_pages, results_per_page)
        summarized_result = "<br>".join(summaries)
        df.at[index, 'summarized_results'] = summarized_result
        
        # Send the summarized results to Groq
        st.write(f"Sending summarized result to Groq for: {query}")
        groq_response = await send_to_groq(summarized_result)
        
        # Handle the response from Groq and update DataFrame
        if 'error' in groq_response:
            df.at[index, 'groq_response'] = groq_response['error']
        else:
            response_message = groq_response.get('choices', [{}])[0].get('message', {}).get('content', None)
            if response_message:
                response_message = re.sub(r"^Here are the key points:.*", "", response_message).strip()
                response_message = response_message.replace('<br>', '\n').strip()
                df.at[index, 'groq_response'] = response_message
            else:
                df.at[index, 'groq_response'] = 'No relevant information available'
        
        # Reset summaries for next entity
        summaries.clear()
    
    # Show preview of the updated DataFrame
    st.write("Updated Data with Summarized Results and Groq Responses:")
    st.dataframe(df)

    # Save the updated DataFrame to a new CSV
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file = save_results(df)  # Save the results as result.csv
    
    return output_file  # Return the filename for downloading

# Step 4: Process Summarized Results with Groq API
GROQ_API_KEY = st.secrets["api_keys"]["groq_api_key"] # Fetch Groq API key securely from secrets.toml
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

async def send_to_groq(summary_text):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Clean up HTML tags in the summary_text
    summary_text_clean = re.sub(r'<[^>]*>', '', summary_text)
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Extract the key points and provide a concise summary of the following text. "
                    f"Return only the main points and do not include any introductory phrases or explanations:\n\n"
                    f"{summary_text_clean}\n\n"
                    "Just provide the key summary points."
                )
            }
        ]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GROQ_API_URL, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    return {'error': f'Failed to get valid response from Groq API. Status code: {response.status}'}
    except Exception as e:
        return {'error': str(e)}

def save_results(df):
    """Process final CSV: remove 'summarized_results' and rename 'groq_response' to 'Search Results'."""
    # Remove the 'summarized_results' column
    if 'summarized_results' in df.columns:
        df.drop(columns=['summarized_results'], inplace=True)
    
    # Rename 'groq_response' column to 'Search Results'
    if 'groq_response' in df.columns:
        df.rename(columns={'groq_response': 'Search Results'}, inplace=True)

    # Save the updated DataFrame to a new CSV file (result.csv)
    result_file = 'result.csv'
    df.to_csv(result_file, index=False, encoding='utf-8')
    
    return result_file  # Return the filename for downloading

# Button to fetch, summarize, and process with Groq in one go
if st.button("Fetch, Summarize and Process with Groq"):
    if 'df' in locals() and main_column:
        # Start the process of fetching, summarizing, and passing to Groq
        output_file = asyncio.run(update_csv_with_summaries_and_groq(df, main_column))
        
        st.success(f"Processing complete. You can download the updated file below:")
        st.download_button("Download Final CSV", data=open(output_file, 'rb'), file_name=output_file, mime="text/csv")
    else:
        st.error("Please upload a CSV or connect a Google Sheet, and select a column.")
