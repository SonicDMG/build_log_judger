"""
This script interacts with the Langflow API to run a specified flow and 
extract scores from the "Judge Output" component.

Modules:
    - logging: Provides logging capabilities.
    - os: Provides a way of using operating system dependent functionality.
    - json: Provides JSON encoding and decoding.
    - requests: Allows sending HTTP requests.
    - coloredlogs: Provides colored logging output.
    - dotenv: Loads environment variables from a .env file.
    - tenacity: Provides retrying capabilities for functions.

Environment Variables:
    - BASE_API_URL: The base URL for the Langflow API.
    - LANGFLOW_ID: The Langflow ID.
    - FLOW_ID: The Flow ID.
    - APPLICATION_TOKEN: The Langflow application token for authorization.
    - ENDPOINT: The named endpoint for the API call.

Functions:
    - run_flow(message: str) -> dict:
        Runs the flow with the given message and returns the judge output component from the flow response.
    - extract_scores(judge_output: dict) -> tuple:
        Extracts scores from the "Judge Output" component.

Usage:
    Ensure that the environment variables are set in a .env file.
    Call the run_flow function with the desired message to run the flow and get the judge output.
    Use the extract_scores function to extract the final score and score detail from the judge output.
"""
import logging
import os
import json
import requests
import coloredlogs
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

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

@retry(
    stop=stop_after_attempt(3),  # Retry once (total of 2 attempts)
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(requests.exceptions.JSONDecodeError)
)
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
        response = requests.post(api_url, json=payload, headers=headers, timeout=90)
        response_json = response.json()
    except requests.exceptions.JSONDecodeError as e:
        logger.error("JSONDecodeError: %s", e)
        logger.debug("Response text: %s", response.text)  # Print the response text for debugging
        response_json = {}
    except requests.exceptions.Timeout as e:
        logger.error("Request timeout: %s", e)
        raise
    except requests.exceptions.RequestException as e:
        logger.error("RequestException: %s", e)
        raise

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
