import time
import logging
from typing import List, Dict, Any
from src.config import NOTION_TOKEN, DATABASE_ID

from src.utils.utils import get_stats, parse_page
from src.utils.notion_client import NotionAPIClient

def  main() -> None:
    """
    Main function to remove duplicate pages from a Notion database and display statistics.
    """
    start_time = time.time()
    notion_client = NotionAPIClient(token=str(NOTION_TOKEN))

    unique_pages: List[str] = []
    count_duplicates: int = 0

    try:
        # Fetch all pages from the Notion database
        pages: List[Dict[str, Any]] = notion_client.query_database(database_id=DATABASE_ID)

        # Process each page for duplicates
        for page in pages:
            name_title = page["properties"]["Name"]["title"][0]["text"]["content"]
            duplicated, count_duplicates = parse_page(name_title, unique_pages, count_duplicates)

            if duplicated:
                notion_client.delete_page(page_id=page["id"])
        
    except Exception as e:
        logging.error(f"An error occurred while processing pages: {e}")
        raise e

    # Display statistics
    get_stats(count_duplicates, unique_pages, total_time=time.time() - start_time)

if __name__ == "__main__":
    main()
