from pprint import pprint

from src.config import NAME_TITLE
from src.utils.utils_requests import create_page, get_pages, modify_page
from src.utils.utils import get_stats, parse_page

def main():
    """
    Main function to remove duplicate pages from a Notion database.
    """

    unique_pages = []
    count_duplicates = 0

    # Retrieve 
    pages = get_pages()

    # Process
    for page in pages:
        props = page["properties"]
        name_title = props[NAME_TITLE]["title"][0]["text"]["content"]
        duplicated, count_duplicates = parse_page(name_title, unique_pages, count_duplicates)
        
        if duplicated:
            modify_page(page_id=page["id"], delete=True)

    # Log statistics
    get_stats(count_duplicates, unique_pages)

if __name__ == "__main__":
    main()