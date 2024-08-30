# Build Log Judge

### You will be Judged!
![judge image](static/cyberpunk_judge.webp)

Build Log Judge is a Generateive AI application using Streamlit.io that allows users to upload various types of files (docx, pdf, txt, md) and get a final score based on the content and quality of the files.


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
    pip install streamlit python-docx pymupdf python-dotenv coloredlogs
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

## File Descriptions

- **app.py**: Main application file that handles file uploads, processes the files, and displays the scores.
- **file_reader.py**: Contains functions to read and process different types of files (docx, pdf, txt, md).

## Dependencies

- Streamlit
- python-docx
- PyMuPDF

## Contact

For support or contributions, please contact [yourname@domain.com](mailto:yourname@domain.com).