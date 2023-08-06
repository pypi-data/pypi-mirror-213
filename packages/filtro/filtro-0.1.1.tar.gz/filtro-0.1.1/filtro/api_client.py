import requests
from typing import Dict

BASE_URL = "http://54.171.93.158:8000"

def mask(input_str: str) -> Dict:
    response = requests.post(f"{BASE_URL}/mask", params={"input_str": input_str})
    response.raise_for_status()
    response = response.json()
    return response["masked_string"], response["mapping"]

def clear(input_str: str, mapping: Dict) -> Dict:
    response = requests.post(
        f"{BASE_URL}/clear", 
        params={"input_str": input_str}, 
        json=mapping, 
        headers={'Content-Type': 'application/json'}
    )
    response.raise_for_status()
    response = response.json()
    return response["clear_string"]
