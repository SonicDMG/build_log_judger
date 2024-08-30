import requests
import json
import os
import logging
import coloredlogs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL")
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
ENDPOINT = os.getenv("ENDPOINT")

# Configure logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

def run_flow(message: str) -> dict:
    """
    Run the flow with the given message and return the judge output.

    Args:
        message (str): The input message to be processed by the flow.

    Returns:
        dict: The judge output component from the flow response.
    """
    if LANGFLOW_ID:
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT or FLOW_ID}"
    else:
        api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT or FLOW_ID}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    if APPLICATION_TOKEN:
        headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    else:
        headers = None
    
    # Log the API call
    logger.info("API call made to: %s", api_url)
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response_json = response.json()
    except requests.exceptions.JSONDecodeError as e:
        logger.error("JSONDecodeError: %s", e)
        logger.debug("Response text: %s", response.text)  # Print the response text for debugging
        response_json = {}

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
    logger.info("Judge Output component extracted")
    
    return judge_output

def extract_scores(judge_output):
    """
    Extract scores from the "Judge Output" component.

    Args:
        judge_output (dict): The judge output component from the flow response.

    Returns:
        tuple: A tuple containing the final score and score detail.
    """
    results = judge_output.get('results', {}).get('message', {}).get('text', 'N/A')
    try:
        results_json = json.loads(results)
        final_score = results_json.get("Final Score", "N/A")
        score_detail = results_json.get("Score Detail", {})
    except json.JSONDecodeError:
        final_score = "N/A"
        score_detail = {}
    return final_score, score_detail