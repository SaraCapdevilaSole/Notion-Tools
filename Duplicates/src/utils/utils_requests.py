import requests
from src.config import DATABASE_ID, ENDPOINT, headers
from src.utils.utils import _get_payload

def _notion_post_request(url: str, payload: dict, headers: dict):
    """
    Helper function to make POST requests to the Notion API.
    """
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to make a POST request to Notion: {e}")
    
def create_page(data: dict, database_id: str = DATABASE_ID, headers: dict = headers):
    """
    Create a new page in the specified Notion database.
    """
    url = f"{ENDPOINT}/pages"
    payload = {"parent": {"database_id": database_id}, "properties": data}
    response = _notion_post_request(url, payload, headers)
    print("Page created:", response)
    return response

def get_pages(database_id: str = DATABASE_ID, headers: dict = headers, num_pages: int = None):
    """
    Retrieve pages from a Notion database.
    If num_pages is None, retrieve all pages, otherwise fetch the specified number.
    """
    url = f"{ENDPOINT}/databases/{database_id}/query"
    get_all = num_pages is None
    page_size = 100 if get_all else min(num_pages, 100)

    payload = {"page_size": page_size}
    results = []

    try:
        data = _notion_post_request(url, payload, headers)
        results.extend(data.get("results", []))

        # Handle pagination
        while data.get("has_more") and get_all:
            payload["start_cursor"] = data.get("next_cursor")
            data = _notion_post_request(url, payload, headers)
            results.extend(data.get("results", []))

    except ValueError as e:
        raise ValueError(f"Failed to retrieve pages: {e}")

    return results
    
def modify_page(page_id: str, data: dict = None, delete: bool = False, headers: dict = headers):
    """
    Modify or delete a page in Notion. 
    Set `delete=True` to archive the page.
    """
    url = f"{ENDPOINT}/pages/{page_id}"
    payload = _get_payload(data, delete)
    try:
        response = requests.patch(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to modify the page: {e}")