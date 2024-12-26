import logging
from typing import List, Tuple
from src.config import VERBOSE

def parse_page(name_title: str, unique_pages: set, count_duplicates: int, verbose: bool = VERBOSE) -> Tuple[bool, int]:
    """
    Parse a page title, check for duplicates, and return the updated duplicate count.

    Args:
        name_title (str): The title of the page to parse.
        unique_pages (set): A set of unique page titles.
        count_duplicates (int): The current count of duplicates.
        verbose (bool): Whether to log duplicates.

    Returns:
        Tuple[bool, int]: A tuple containing:
            - A boolean indicating if the page is a duplicate.
            - The updated count of duplicates.

    Logs:
        - Duplicate found if verbose is enabled
    """
    # Create a unique identifier for the page
    normalised_name = name_title.lower().replace(" ", "")

    # Check if the page is a duplicate
    is_duplicate = normalised_name in unique_pages
    
    # Add the page to the unique pages set if it's not already there
    unique_pages.add(normalised_name)

    # Increment count if duplicate
    count_duplicates += int(is_duplicate)
    
    # Log the duplicate if verbose is enabled
    if is_duplicate and verbose:
        logging.info(f"Duplicate found -> '{name_title}'")

    return is_duplicate, count_duplicates


def get_stats(count_duplicates: int, unique_pages: set, total_time: float) -> None:
    """
    Print statistics on duplicates found in the Notion database.

    Args:
        count_duplicates (int): The count of duplicate pages.
        unique_pages (set): The set of unique pages.
        total_time (float): The total time taken to process the pages.

    Logs:
        - Total count of pages
        - Percentage of duplicates
        - Total time taken
    """
    total_count = len(unique_pages) + count_duplicates
    if not total_count:
        logging.warning("No database entries found")
        return
    
    prop = int(count_duplicates * 100 / total_count)
    logging.info(f'Process finished, stats summary: \n- Duplicates Found: {count_duplicates}/{total_count} ({prop}%) \n- Total time taken: {total_time:.1f} s')
