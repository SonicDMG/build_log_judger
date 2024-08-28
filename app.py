import streamlit as st
import docx
import fitz  # PyMuPDF
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL")
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
ENDPOINT = os.getenv("ENDPOINT")

def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT or FLOW_ID}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    
    # Log the API call
    print("API call made to:", api_url)
    
    response = requests.post(api_url, json=payload, headers=headers)
    response_json = response.json()
    
    # Initialize default values
    judge_output = {
        'component_display_name': 'N/A',
        'results': {
            'message': {
                'text': 'N/A'
            }
        }
    }
    
    # Extracting "Judge Output" component
    outputs = response_json.get('outputs', [])
    if not outputs:
        return judge_output

    for output in outputs[0].get('outputs', []):
        component_display_name = output.get('component_display_name', '')
        if component_display_name == "Judge Output":
            judge_output = output
            break
    
    # Log the extraction of "Judge Output"
    print("Judge Output component extracted")
    
    return judge_output

def read_docx(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    full_text = []
    for page in doc:
        full_text.append(page.get_text())
    return '\n'.join(full_text)

def read_txt(file):
    return file.read().decode("utf-8")

def read_md(file):
    return file.read().decode("utf-8")

def read_file(file, file_type):
    if file_type == "docx":
        content = read_docx(file)
    elif file_type == "pdf":
        content = read_pdf(file)
    elif file_type == "txt":
        content = read_txt(file)
    elif file_type == "md":
        content = read_md(file)
    else:
        return "Unsupported file type"
    
    # Log the content being sent to the API
    print(f"Content from {file_type} file read and sent to API")
    
    response = run_flow(content)
    
    # Log the response received from the API
    print("Response received from API")
    
    return response

def extract_scores(judge_output):
    # Extract scores from the "Judge Output" component
    scores = judge_output.get('results', {}).get('message', {}).get('text', 'N/A')
    return scores

# Streamlit app
st.title("Document Reader and API Integration")

uploaded_files = st.file_uploader("Choose a file", type=["docx", "pdf", "txt", "md"], accept_multiple_files=True)
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]
        
        with st.spinner(f"Reading {uploaded_file.name}..."):
            response = read_file(uploaded_file, file_type)
        
        # Extract and display scores
        scores = extract_scores(response)
        
        # Display file name and page title as section headers with color coding
        st.markdown(f"<h2 style='color:#00ffff;'>File: {uploaded_file.name}</h2>", unsafe_allow_html=True)
        st.write(scores)