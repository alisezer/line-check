"""Data Retrieval Module"""

import logging

import requests

logger = logging.getLogger(__name__)


def form_url(line):
    return f"https://api.tfl.gov.uk/Line/{line}/Disruption"

def retrieve_line_data(line):
    logger.info(f"Retrieving line disruption results for {line}")
    url = form_url(line)
    result = requests.get(url)
    return result.json()
