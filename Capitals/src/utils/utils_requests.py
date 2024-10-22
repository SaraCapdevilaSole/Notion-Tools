import requests
from src.config import DATABASE_ID, ENDPOINT, headers, VERBOSE

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
    if VERBOSE:
        print("\nPage created:", response)
    return response