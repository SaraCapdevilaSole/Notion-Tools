import logging
from src.config import DATE_TEMPLATE, VERBOSE

def parse_page(name_title: str, unique_pages: list, count_duplicates: int, verbose: bool = VERBOSE):
    """
    Parse a page title, check for duplicates, and return the updated duplicate count.
    """
    normalised_name = _create_unique_identifier(name_title)
    is_duplicate = normalised_name in unique_pages
    count_duplicates += int(is_duplicate) # increment count if duplicate
    if is_duplicate and verbose:
        logging.info(f"Duplicate found -> '{name_title}'")
    else:
        unique_pages.append(normalised_name)
    return is_duplicate, count_duplicates

def _create_unique_identifier(title: str):
    """
    Generate a unique identifier by normalizing the page title.
    """
    return title.lower().replace(" ", "")

def get_stats(duplicates_count: int, non_duplicates_count: int, total_time: float):
    """
    Print statistics on duplicates found in the Notion database.
    """
    total_count = non_duplicates_count + duplicates_count
    if not total_count:
        logging.warning("No database entries found")
        return
    
    prop = int(duplicates_count * 100 / total_count)
    logging.info(f'\nDuplicates Found: {duplicates_count}/{total_count} ({prop}%) | Total time taken: {total_time:.1f} s')

def fetch_template(name: str, property_type: str, data):
    """
    Fetch a Notion property template for different data types.
    """
    def property_template(data, property_type):
        if property_type == 'DATETIME':
            return DATE_TEMPLATE(*data)
        elif property_type == 'TEXT':
            return [{"text": {"content": data}}]
    
    return {
        name: {property_type: property_template(data, property_type)}
    }




