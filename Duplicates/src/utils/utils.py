from datetime import datetime, timezone
from src.config import DATE_TEMPLATE, VERBOSE

def _get_payload(data: dict, delete: bool):
    """
    Construct the payload for modifying or deleting a page.
    """
    if delete:
        return {"archived": True}
    return {"properties": data}

def get_date():
    """
    Return the current date and time in ISO format (UTC).
    """
    return datetime.now().astimezone(timezone.utc).isoformat()

def parse_page(name_title: str, unique_pages: list, count_duplicates: int, verbose: bool = VERBOSE):
    """
    Parse a page title, check for duplicates, and return the updated duplicate count.
    """
    normalized_name = _create_unique_identifier(name_title)
    if normalized_name in unique_pages:
        if verbose:
            print(f"Duplicate found -> '{name_title}'")
        count_duplicates += 1
        return True, count_duplicates
    else:
        unique_pages.append(normalized_name)
        return False, count_duplicates

def _create_unique_identifier(title: str):
    """
    Generate a unique identifier by normalizing the page title.
    """
    return title.lower().replace(" ", "")

def get_stats(dups_counts: int, list_nondups: list):
    """
    Print statistics on duplicates found in the Notion database.
    """
    total_count = len(list_nondups) + dups_counts
    if total_count == 0:
        print("Error: No database entries found")
        return
    
    prop = int(dups_counts * 100 / total_count)
    print(f'\nDuplicates Found: {dups_counts}/{total_count} ({prop}%)')

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




