from datetime import datetime, timezone

from src.config import DATE_TEMPLATE

def _get_payload(data, delete):
    if delete:
        # Delete page
        payload = {"archived": True}
    else:
        # Update page
        payload = {"properties": data} 
    return payload

def get_date():
    return datetime.now().astimezone(timezone.utc).isoformat()

def parse_page(name_title, unique_pages, count_duplicates):
    normalised_name = _create_unique_identifier(name_title)
    if normalised_name in unique_pages:
        print(f"Duplicate found for -> {name_title}")
        count_duplicates += 1
        duplicated = True
    else:
        unique_pages.append(normalised_name)
        duplicated = False
    return duplicated, count_duplicates

def _create_unique_identifier(title):
    return title.lower().replace(" ", "")

def get_stats(dups_counts, list_nondups):
    total_count = len(list_nondups)+dups_counts
    prop = int(dups_counts*100/(total_count))
    print(f'\nDuplicates Found: {dups_counts}/{total_count} ({prop}%)')

def fetch_template(name, property_type, data):
    """
    name: name of column, 
    data: value in column/row, 
    property_type: property type [PROPERTY_TYPES].
    """
    def property_template(data, property_type):
        if property_type == 'DATETIME':
            return DATE_TEMPLATE(*data)
        elif property_type == 'TEXT':
            return [{"text": {"content": data}}]

    return {
        name: {property_type: property_template(data, property_type)} 
    }




