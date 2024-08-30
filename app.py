import os
import logging
import streamlit as st
import coloredlogs
from file_reader import read_file
from dropbox_reader import list_dropbox_files_and_folders, download_dropbox_file
from langflow_api import run_flow, extract_scores
from scoreboard import display_scoreboard

# Configure logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Streamlit app

# List to store file names and final scores
scoreboard = []

st.image("static/ascii-art.png", width=300)

# Option to choose file source
file_source = st.radio("Choose file source", ("Local", "Dropbox"))

if file_source == "Local":
    uploaded_files = st.file_uploader("Choose a file", type=["docx", "pdf", "txt", "md"], accept_multiple_files=True)
    for uploaded_file in uploaded_files:
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
            st.markdown(f"<h2 id='{uploaded_file.name}' style='color:#00ffff;'>File: {uploaded_file.name}</h2>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:#ff00ff;'>Final Score: {final_score}</h3>", unsafe_allow_html=True)
            
            # Display Score Detail
            st.markdown("<h3 style='color:#ff00ff;'>Score Detail</h3>", unsafe_allow_html=True)
            for key, value in score_detail.items():
                st.markdown(f"**{key}**: {value}")

elif file_source == "Dropbox":
    folder_path = '/rag++ hack night - build log submissions'  # Specific folder
    dropbox_files, dropbox_folders = list_dropbox_files_and_folders(folder_path)
    
    if dropbox_files:
        selected_files = st.multiselect("Choose files from Dropbox", dropbox_files)
        
        for file_name in selected_files:
            file_content = download_dropbox_file(file_name)
            if file_content:
                file_type = file_name.split('.')[-1]
                
                with st.spinner(f"Reading {os.path.basename(file_name)}..."):
                    content = read_file(file_content, file_type)
                    response = run_flow(content)
                
                # Extract and display scores
                final_score, score_detail = extract_scores(response)
                
                # Add to scoreboard
                scoreboard.append((os.path.basename(file_name), final_score))
                
                # Display file name and page title as section headers with color coding
                st.markdown(f"<h2 id='{os.path.basename(file_name)}' style='color:#00ffff;'>File: {os.path.basename(file_name)}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color:#ff00ff;'>Final Score: {final_score}</h3>", unsafe_allow_html=True)
                
                # Display Score Detail
                st.markdown("<h3 style='color:#ff00ff;'>Score Detail</h3>", unsafe_allow_html=True)
                for key, value in score_detail.items():
                    st.markdown(f"**{key}**: {value}")

# Sort scoreboard by final score in descending order
def get_score(score):
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
    st.title("You will be judged!")
    st.image("static/cyberpunk_judge.png")
    st.caption("Powered by DataStax Langflow and Streamlit.io")
    #st.title("Scoreboard")

    # Use the display_scoreboard function from scoreboard.py
    display_scoreboard(scoreboard)
