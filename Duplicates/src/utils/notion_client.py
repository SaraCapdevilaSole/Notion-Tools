import logging
from functools import wraps
from typing import Any, Callable

import requests


def log_errors(description: str) -> Callable:
    """
    Decorator to log errors with a custom description.

    Args:
        description (str): A description of the context where the error occurred.

    Returns:
        Callable: The decorated function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"{description}: {e}")
                raise

        return wrapper

    return decorator


class NotionAPIClient:
    """
    A client to interact with the Notion API.
    Encapsulates common operations like querying databases, creating pages, updating pages, and deleting pages.
    """

    def __init__(self, token: str, base_url: str = "https://api.notion.com/v1", version: str = "2022-06-28"):
        """
        Initialise the NotionAPIClient.

        Args:
            token (str): Notion API authentication token.
            base_url (str): The base URL for the Notion API. Defaults to "https://api.notion.com/v1".
            version (str): The Notion API version. Defaults to "2022-06-28".
        """
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": version,
        }

    def _notion_post_request(self, url: str, payload: dict) -> Any:
        """
        Helper function to make POST requests to the Notion API.

        Args:
            url (str): The Notion API endpoint.
            payload (dict): The data to send in the POST request.

        Returns:
            Any: The response from the Notion API containing the created page data.
        """
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def _notion_patch_request(self, url: str, payload: dict) -> Any:
        """
        Helper function to make PATCH requests to the Notion API.

        Args:
            url (str): The Notion API endpoint.
            payload (dict): The data to send in the POST request.

        Returns:
            Any: The response from the Notion API containing the updated page data.
        """
        response = requests.patch(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    # get_pages
    @log_errors("Failed to retrieve pages")
    def query_database(self, database_id: str, num_pages: int = 100) -> list[dict]:
        """
        Query a Notion database and retrieve pages.

        Args:
            database_id (str): The ID of the Notion database to query.
            num_pages (int): The maximum number of pages to retrieve.

        Returns:
            list[dict]: A list of pages retrieved from the database.
        """
        url = f"{self.base_url}/databases/{database_id}/query"
        page_size = min(num_pages, 100)

        payload = {"page_size": page_size}
        results = []

        data = self._notion_post_request(url, payload)
        results.extend(data.get("results", []))

        # Handle pagination
        while data.get("has_more"):
            next_cursor = data.get("next_cursor")
            if next_cursor is None:
                break
            payload["start_cursor"] = next_cursor
            data = self._notion_post_request(url, payload)
            results.extend(data.get("results", []))

        return results

    @log_errors("Failed to create a page")
    def create_page(self, database_id: str, properties: dict[str, Any]) -> None:
        """
        Create a new page in a Notion database.

        Args:
            database_id (str): The ID of the Notion database where the page will be created.
            properties (Dict[str, Any]): The properties of the page.
        """
        url = f"{self.base_url}/pages"
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties,
        }
        self._notion_post_request(url, payload)

    @log_errors("Failed to update a page")
    def update_page(self, page_id: str, properties: dict[str, Any]) -> Any:
        """
        Update a page in Notion.

        Args:
            page_id (str): The ID of the Notion page to update.
            properties (dict[str, Any]): The properties to update.

        Returns:
            Any: The response from the Notion API containing the updated page data.
        """
        url = f"{self.base_url}/pages/{page_id}"
        payload = {"properties": properties}
        return self._notion_patch_request(url, payload)

    @log_errors("Failed to delete a page")
    def delete_page(self, page_id: str) -> Any:
        """
        Delete (archive) a page in Notion.

        Args:
            page_id (str): The ID of the Notion page to delete.

        Returns:
            Any: The response from the Notion API containing the deleted page data.
        """
        url = f"{self.base_url}/pages/{page_id}"
        payload = {"archived": True}
        return self._notion_patch_request(url, payload)
