import requests
import json

from src.config import DATABASE_ID, ENDPOINT, headers
from src.utils.utils import _get_payload

def create_page(data: dict, DATABASE_ID: str=DATABASE_ID, headers: str=headers):
    url = f'{ENDPOINT}/pages'

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(url, headers=headers, json=payload)
    print(res.status_code)
    return res

def get_pages(DATABASE_ID: str=DATABASE_ID, headers: str=headers, num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"{ENDPOINT}/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results

def modify_page(page_id: str, data:dict=None, delete=False):
    url = f"{ENDPOINT}/pages/{page_id}"
    payload = _get_payload(data, delete)
    res = requests.patch(url, json=payload, headers=headers)
    return res