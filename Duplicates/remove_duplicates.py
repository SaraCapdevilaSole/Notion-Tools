from src.config import NAME_TITLE
from src.utils.utils_requests import create_page, get_pages, modify_page
from src.utils.utils import get_stats, parse_page

def fetch_and_process_pages():
    """
    Fetch all pages from the Notion database and process them to detect and remove duplicates.
    
    Returns:
        unique_pages (list): A list of unique page names.
        count_duplicates (int): The number of duplicates found.
    """
    unique_pages = []
    count_duplicates = 0

    try:
        # Fetch all pages from the Notion database
        pages = get_pages()

        # Process each page for duplicates
        for page in pages:
            name_title = page["properties"][NAME_TITLE]["title"][0]["text"]["content"]
            duplicated, count_duplicates = parse_page(name_title, unique_pages, count_duplicates)

            if duplicated:
                modify_page(page_id=page["id"], delete=True)
        
    except Exception as e:
        print(f"An error occurred while processing pages: {e}")

    return unique_pages, count_duplicates

def main():
    """
    Main function to remove duplicate pages from a Notion database and display statistics.
    """
    unique_pages, count_duplicates = fetch_and_process_pages()

    get_stats(count_duplicates, unique_pages)

if __name__ == "__main__":
    main()
