# Build Log Judge

### You will be Judged!
![judge image](static/cyberpunk_judge.webp)

Build Log Judge is a Generative AI application using [Langflow](https://www.langflow.org/) and [Streamlit.io](https://streamlit.io/) that allows users to upload various types of files (docx, pdf, txt, md) and get a final score based on the content and quality of the files. 

The prompt template and URLs used in the build_log_judger.json file in Langflow are specifically tuned to look for products releated to DataStax and our partners. You can tune this yourself by updating the vendor list and URL components in Langflow.

## Installation

### Prerequisites

- Python 3.11
- pip (Python package installer)

### Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/SonicDMG/build_log_judger.git
    cd build_log_judge
    ```

2. **Create a virtual environment**:
    ```sh
    python3.11 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Activate the virtual environment** (if not already activated):
    ```sh
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Run the Streamlit application**:
    ```sh
    streamlit run app.py
    ```

3. **Upload Files**: Use the file uploader in the web interface to upload your files and get the scores.

## Environment Variables

1. **Create a copy of the `.env.example` file as your `.env` file**:
    ```sh
    cp .env.example .env
    ```

2. **Edit the `.env` file**: Add the following environment variables with your own values:

```properties
#### Dropbox access
DROPBOX_ACCESS_TOKEN=your_dropbox_access_token_here
DROPBOX_FOLDER_PATH='/your_dropbox_folder_path_here'

#### Generative AI using Langflow
ENDPOINT=your_flow_endpoint_name_here

# Local Langflow
BASE_API_URL=http://127.0.0.1:7860

# DataStax Astra
#BASE_API_URL=https://your_datastax_astra_url_here
#LANGFLOW_ID=your_langflow_id_here
#APPLICATION_TOKEN=your_application_token_here