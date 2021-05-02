"""Data Retrieval Module"""

import logging

import requests

logger = logging.getLogger(__name__)

def retrieve_line_data(line):
    url = f"https://api.tfl.gov.uk/Line/{line}/Disruption"
    result = requests.get(url)
    return result.json()
