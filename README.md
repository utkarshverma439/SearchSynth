# SearchSynth

**SearchSynth** is an advanced web search and summarization tool that fetches search results from **SerpApi**, processes them to extract key information, and then further summarizes the results using **Groq** API. This app allows users to upload a CSV or connect a Google Sheet, specify a search query, and get summarized search results in a downloadable CSV format.

## Features
- **CSV Upload**: Upload your CSV with search queries or connect directly to a Google Sheet.
- **Web Search**: Uses **SerpApi** to fetch search results based on your queries.
- **Summarization**: Processes the search results and summarizes them.
- **Groq Integration**: Sends the summarized results to **Groq** API for further refinement.
- **Download Results**: Allows you to download a CSV with the final summarized search results.

---

## Table of Contents

1. [Technologies Used](#technologies-used)
2. [Installation](#installation)
3. [Setup and Configuration](#setup-and-configuration)
4. [How to Use](#how-to-use)
5. [API Keys](#api-keys)
6. [Licensing](#licensing)
7. [Contributing](#contributing)

---

## Technologies Used

- **Python 3.x**: Core language for the project.
- **Streamlit**: For building the web-based user interface.
- **pandas**: For data manipulation and handling CSV/Google Sheets data.
- **gspread**: To interact with Google Sheets API.
- **aiohttp**: For asynchronous HTTP requests.
- **SerpApi**: For fetching search results from Google search.
- **Groq API**: For further summarizing and processing search results using an AI language model.

---

## Installation

### Prerequisites

- Python 3.x
- An IDE or text editor (e.g., Visual Studio Code, PyCharm)
- Internet connection to access APIs

### Steps to Install

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SearchSynth.git
   cd SearchSynth
   ```

2. Install the required dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `credentials.json` file for Google Sheets authentication (more details below).
   
4. Set up your API keys for **SerpApi** and **Groq** (explained in the next section).

---

## Setup and Configuration

### Google Sheets Setup

1. Create a project on [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Enable the **Google Sheets API** and the **Google Drive API**.
3. Create a service account and download the `credentials.json` file.
4. Share your Google Sheet with the email address provided in your `credentials.json`.

### API Keys

You will need to get your API keys for **SerpApi** and **Groq**.

#### 1. **SerpApi**
- Sign up and generate your API key at [SerpApi](https://serpapi.com/).
  
#### 2. **Groq**
- Create an account on [Groq](https://www.groq.com/) and get your API key.

### Adding Your API Keys to Streamlit

1. Create a `secrets.toml` file in the `.streamlit` directory (create the directory if it doesn't exist).

2. Add your API keys in the `secrets.toml` like this:

   ```toml
   [api_keys]
   serpapi_api_key = "YOUR_SERPAPI_KEY"
   groq_api_key = "YOUR_GROQ_API_KEY"
   ```

---

## How to Use

### Step 1: Upload CSV or Connect Google Sheet

- **Upload CSV**: You can upload a CSV file containing your search queries.
  - The CSV should have one column with search query terms.
  
- **Connect Google Sheet**: You can connect to your Google Sheet by entering the sheet URL. Ensure the sheet has a column containing the search queries.

### Step 2: Define Search Query Template

- Enter the template for the query you want to search. For example: `"What is the best programming language for AI?"`.
  
### Step 3: Fetch and Summarize Results

- Click **Fetch and Summarize Results** to retrieve search results for each query. The app will fetch data from **SerpApi** and display a summarized view.
  
### Step 4: Process with Groq and Download Result

- After summarizing the results, click **Process with Groq and Download Result** to further refine the summaries using the **Groq** API.
- The results will be saved in a downloadable CSV file with a column named **Search Results** containing the final summaries.

---

## API Keys

To use **SearchSynth**, you need API keys for **SerpApi** and **Groq**.

### How to Get API Keys

1. **SerpApi**: 
   - Go to [SerpApi](https://serpapi.com/manage-api-key), sign up, and get your free or paid API key.
   
2. **Groq**:
   - Go to [Groq](https://console.groq.com/keys), sign up, and get your API key for AI processing.

Once you have the API keys, store them in the `secrets.toml` file as mentioned in the **Setup and Configuration** section.

---

## Licensing

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Contributing

We welcome contributions! If you'd like to improve the project, feel free to fork the repository, create a branch, and submit a pull request. Please follow these guidelines for contributions:

1. **Bug Fixes**: Create a new branch for any bug fixes or improvements.
2. **Documentation**: If you're adding new features or changing existing ones, please update the README file.
3. **Testing**: Ensure all tests pass before submitting a pull request.
4. **Code Style**: Follow PEP8 and write clean, understandable code.

---

## Acknowledgements

- **SerpApi**: For providing a powerful API to fetch real-time Google search results.
- **Groq**: For its AI-powered summarization capabilities that help improve the quality of search result summaries.

---

## Contact

If you have any questions or suggestions, feel free to open an issue or contact me directly via [GitHub Issues](https://github.com/utkarshverma439/SearchSynth/issues) or [LinkedIn](https://www.linkedin.com/in/utkarshverma439/).

---

### Links

- [SerpApi Documentation](https://serpapi.com/search-api)
- [Groq API Documentation](https://console.groq.com/docs/overview)

---

### Final Thoughts

Thank you for checking out **SearchSynth**! It's a tool built to make web search and summarization easy and efficient. We hope this project helps you streamline your search process and get actionable insights with minimal effort. Feel free to contribute, suggest improvements, and make it even better!

---

### Example of the structure:

```plaintext
- /app.py                      # Main app file with Streamlit interface
- /requirements.txt            # Python dependencies
- /.streamlit/secrets.toml     # API keys for SerpApi and Groq
- /LICENSE                     # License file for the project
- /README.md                   # This README file
```

