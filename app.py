"""
This script is a Streamlit application for processing and displaying scores of documents.

The application supports the following features:
1. Users can upload multiple files from their local system or select files from Dropbox.
2. The uploaded or selected files are processed to extract their content and compute scores.
3. A progress bar is displayed to indicate the progress of file processing.
4. The scores of the processed files are displayed in a scoreboard, sorted in descending order.

The script uses the following libraries:
- `streamlit` for creating the web application.
- `coloredlogs` for enhanced logging.
- `file_reader` for reading the content of various file types.
- `dropbox_reader` for interacting with Dropbox.
- `langflow_api` for running the flow and extracting scores.
- `scoreboard` for displaying the scoreboard.

Functions:
- `get_score(score)`: Helper function to extract the numeric score from a score string.

Example usage:
    Run the script using Streamlit:
    ```
    streamlit run app.py
    ```
"""
import logging
import streamlit as st
import coloredlogs
from dropbox.exceptions import AuthError
from file_reader import read_file
from dropbox_reader import (
    list_dropbox_files_and_folders,
    download_dropbox_file,
    DROPBOX_AUTHENTICATED
)
from langflow_api import run_flow, extract_scores
from scoreboard import display_scoreboard

# Configure logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

# ASCII art to be logged at the start of the app
ASCII_ART = """
██████╗ ██╗   ██╗██╗██╗     ██████╗     ██╗      ██████╗  ██████╗ 
██╔══██╗██║   ██║██║██║     ██╔══██╗    ██║     ██╔═══██╗██╔════╝ 
██████╔╝██║   ██║██║██║     ██║  ██║    ██║     ██║   ██║██║  ███╗
██╔══██╗██║   ██║██║██║     ██║  ██║    ██║     ██║   ██║██║   ██║
██████╔╝╚██████╔╝██║███████╗██████╔╝    ███████╗╚██████╔╝╚██████╔╝
╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝     ╚══════╝ ╚═════╝  ╚═════╝ 
                                                                  
     ██╗██╗   ██╗██████╗  ██████╗ ███████╗██████╗ ██╗             
     ██║██║   ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗██║             
     ██║██║   ██║██║  ██║██║  ███╗█████╗  ██████╔╝██║             
██   ██║██║   ██║██║  ██║██║   ██║██╔══╝  ██╔══██╗╚═╝             
╚█████╔╝╚██████╔╝██████╔╝╚██████╔╝███████╗██║  ██║██╗             
 ╚════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝             
"""

# Log the ASCII art
logger.info(ASCII_ART)

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Streamlit app

# List to store file names and final scores
scoreboard = []

# Flag to check if all documents are processed
ALL_DOCUMENTS_PROCESSED = False

st.image("static/ascii-art.png", width=200)

# Option to choose file source
file_source_options = ["Local"]
if DROPBOX_AUTHENTICATED:
    file_source_options.append("Dropbox")

# Option to choose file source
file_source = st.radio("Choose file source", file_source_options)

# Create a placeholder for the progress bar
progress_bar = st.progress(0)

if file_source == "Local":
    uploaded_files = st.file_uploader("Choose a file",
                                      type=["docx", "pdf", "txt", "md"],
                                      accept_multiple_files=True)
    if uploaded_files:
        total_files = len(uploaded_files)
        #progress_bar = st.sidebar.progress(0)
        for i, uploaded_file in enumerate(uploaded_files):
            if uploaded_file is not None:
                file_type = uploaded_file.name.split('.')[-1]

                with st.spinner(f"Reading {uploaded_file.name}..."):
                    content = read_file(uploaded_file, file_type)
                    response = run_flow(content)

                # Extract and display scores
                final_score, score_detail = extract_scores(response)

                # Add to scoreboard
                scoreboard.append((uploaded_file.name, final_score))

                # Display file name and page title as section headers with color coding
                st.markdown(
                    f"<h2 id='{uploaded_file.name}' style='color:#00ffff;'>"
                    f"File: {uploaded_file.name}</h2>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<h3 style='color:#ff00ff;'>Final Score: {final_score}</h3>",
                    unsafe_allow_html=True
                )

                # Display Score Detail
                st.markdown("<h3 style='color:#ff00ff;'>Score Detail</h3>", unsafe_allow_html=True)
                for key, value in score_detail.items():
                    st.markdown(f"**{key}**: {value}")

                # Update progress bar
                progress_bar.progress((i + 1) / total_files)
        ALL_DOCUMENTS_PROCESSED = True

elif file_source == "Dropbox":
    try:
        FOLDER_PATH = '/rag++ hack night - build log submissions'  # Specific folder
        file_map, dropbox_folders = list_dropbox_files_and_folders(FOLDER_PATH)

        if file_map:
            file_names = list(file_map.keys())
            selected_files = st.multiselect("Choose files from Dropbox", file_names)

            if selected_files:
                total_files = len(selected_files)
                for i, file_name in enumerate(selected_files):
                    file_path = file_map[file_name]
                    file_content = download_dropbox_file(file_path)
                    if file_content:
                        file_type = file_name.split('.')[-1]

                        with st.spinner(f"Reading {file_name}..."):
                            content = read_file(file_content, file_type)
                            response = run_flow(content)

                        # Extract and display scores
                        final_score, score_detail = extract_scores(response)

                        # Add to scoreboard
                        scoreboard.append((file_name, final_score))

                        # Display file name and page title as section headers with color coding
                        st.markdown(
                            f"<h2 id='{file_name}' style='color:#00ffff;'>File: {file_name}</h2>", 
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<h3 style='color:#ff00ff;'>Final Score: {final_score}</h3>", 
                            unsafe_allow_html=True
                        )

                        # Display Score Detail
                        st.markdown(
                            "<h3 style='color:#ff00ff;'>Score Detail</h3>", 
                            unsafe_allow_html=True
                        )
                        for key, value in score_detail.items():
                            st.markdown(f"**{key}**: {value}")

                        # Update progress bar
                        progress_bar.progress((i + 1) / total_files)
                ALL_DOCUMENTS_PROCESSED = True
    except AuthError as err:
        st.error(
            "Dropbox authentication error: The access token has expired. "
            "Please refresh the access token."
        )
        st.stop()  # Stop further execution


# Sort scoreboard by final score in descending order
def get_score(score):
    """
    Extract the numeric score from a score string.

    This function takes a score, which can be an integer or a string in the format "X/Y",
    and returns the numeric value of the score. If the score is already an integer, it is
    returned as is. If the score is a string, the function attempts to extract the numeric
    value before the '/' character. If the extraction fails, a default value of 0 is returned.

    Args:
        score (int or str): The score to be processed. 
        It can be an integer or a string in the format "X/Y".

    Returns:
        int: The numeric value of the score, or 0 if the extraction fails.
    """
    if isinstance(score, int):
        return score
    try:
        return int(score.split('/')[0])
    except ValueError:
        return 0  # Default value for invalid scores


# Sort scoreboard by final score in descending order
scoreboard.sort(key=lambda x: get_score(x[1]), reverse=True)

# Display scoreboard
with st.sidebar:
    if ALL_DOCUMENTS_PROCESSED:
        st.title("You have been judged!")
        st.image("static/cyberpunk_judge_pointing.webp", width=500)
    else:
        st.title("You will be judged!")
        st.image("static/cyberpunk_judge.webp", width=500)
    st.caption("Powered by DataStax Langflow and Streamlit.io")

    display_scoreboard(scoreboard)
