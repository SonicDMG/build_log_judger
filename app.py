import streamlit as st
from file_reader import read_file
from langflow_api import run_flow, extract_scores

# Streamlit app

# List to store file names and final scores
scoreboard = []

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
        st.markdown(f"<h2 style='color:#00ffff;'>File: {uploaded_file.name}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#ff00ff;'>Final Score: {final_score}</h3>", unsafe_allow_html=True)
        
        # Display Score Detail
        st.markdown(f"<h3 style='color:#ff00ff;'>Score Detail</h3>", unsafe_allow_html=True)
        for key, value in score_detail.items():
            st.markdown(f"**{key}**: {value}")

# Sort scoreboard by final score in descending order
def get_score(score):
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
    st.title("Scoreboard")

    for file_name, final_score in scoreboard:
        st.sidebar.markdown(f"**{file_name}**: {final_score}")