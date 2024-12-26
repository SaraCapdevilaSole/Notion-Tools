import logging
from typing import List, Tuple
from src.config import VERBOSE

def parse_page(name_title: str, unique_pages: list, count_duplicates: int, verbose: bool = VERBOSE) -> Tuple[bool, int]:
    """
    Parse a page title, check for duplicates, and return the updated duplicate count.

    Args:
        name_title (str): The title of the page to parse.
        unique_pages (list): A list of unique page titles.
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
    count_duplicates += int(is_duplicate)  # Increment count if duplicate
    
    if is_duplicate:
        # Log the duplicate if verbose is enabled
        if verbose:
            logging.info(f"Duplicate found -> '{name_title}'")
    else:
        # Add the page to the unique pages list
        unique_pages.append(normalised_name)

    return is_duplicate, count_duplicates


def get_stats(count_duplicates: int, unique_pages: List[str], total_time: float) -> None:
    """
    Print statistics on duplicates found in the Notion database.

    Args:
        count_duplicates (int): The count of duplicate pages.
        unique_pages (List[str]): The list of unique pages.
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
    logging.info(f'\nProcess finished, stats summary: \n\tDuplicates Found: {count_duplicates}/{total_count} ({prop}%) \n\tTotal time taken: {total_time:.1f} s')
