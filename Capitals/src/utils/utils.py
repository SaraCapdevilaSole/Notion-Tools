import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
import copy
import re

from src.config import CONTINENTS, DB_TEMPLATE, URL, VERBOSE
from src.utils.utils_requests import create_page

def _get_text(cell: BeautifulSoup) -> str:
    """Extract clean text from the table cell, preserving spaces between elements."""
    return ' '.join(cell.get_text().split())

def is_country(cell: BeautifulSoup) -> Optional[str]:
    """Check if the cell contains a country (with flag icon)."""
    if cell.find('span', {'class': 'flagicon'}):
        return True
    return None

def is_continent(text: str) -> Optional[str]:
    """Check if the cell contains a continent name."""
    return text if text in CONTINENTS else None

def is_note(text: str) -> Optional[str]:
    """Check if the cell contains a note (e.g., longer text or specific keywords)."""
    return '.' in text

def _detect_cell_type(cell: BeautifulSoup, classified_row: List[Dict[str, Optional[str]]]) -> Tuple[Optional[str], Optional[str]]:
    """Identify the type of content in the cell: country, continent, note, or capital."""
    cell_text, cell_type = _get_text(cell), None

    country = is_country(cell)
    continent = is_continent(cell_text)
    note = is_note(cell_text)

    if country and not classified_row['country']:
        cell_type = 'country'
    elif continent and not classified_row['continent']:
        cell_type = 'continent'
    elif note and not classified_row['note']:
        cell_type = 'note'
    elif cell_text and not classified_row['capital']:
        cell_type = 'capital'
    return cell_type, cell_text

def row_classifier(cells: List[BeautifulSoup]) -> Dict[str, Optional[str]]:
    classified_row = copy.deepcopy(DB_TEMPLATE)
    for cell in cells:
        cell_type, cell_text = _detect_cell_type(cell, classified_row)
        
        if cell_type in classified_row: 
            rowspan_value = cell.get('rowspan')
            if rowspan_value:
                classified_row['rowspan'][cell_type] = int(rowspan_value)
            classified_row[cell_type] = cell_text
    return classified_row

def fetch_html_content(url: str) -> bytes:
    """Fetch the HTML content from the given URL."""
    response = requests.get(url)
    response.raise_for_status() 
    return response.content

def parse_table(soup: BeautifulSoup) -> BeautifulSoup:
    """Find and return the target table from the soup object."""
    return soup.find('table', {'class': 'wikitable'})

def extract_rows(table: BeautifulSoup) -> List[BeautifulSoup]:
    """Extract rows of interest from the table."""
    return table.find_all('tr')

def _remove_rowspan(capitals: List[Dict[str, Optional[str]]]) -> List[Dict[str, Optional[str]]]:
    """Remove 'rowspan' entry from dictionary."""
    for entry in capitals:
        entry.pop('rowspan', None)
    return capitals

def fetch_world_capitals():
    world_capitals = []

    html_content = fetch_html_content(URL)
    soup = BeautifulSoup(html_content, 'html.parser')

    table = parse_table(soup)
    rows_of_interest = extract_rows(table)

    for row in rows_of_interest:
        cells = row.find_all('td')
        if len(cells) > 0:
            classified_country = row_classifier(cells)
            world_capitals.append(classified_country)
            del classified_country
            
    return world_capitals

def _fill_db(capitals: List[Dict[str, Optional[str]]]) -> None:
    """Fill missing values in the DB based on rowspan."""
    for i, current in enumerate(capitals):
        for field, rowspan_value in current['rowspan'].items():
            for j in range(i + 1, i + rowspan_value):
                if j < len(capitals):
                    next_entry = capitals[j]
                    if next_entry[field] is None:
                        if VERBOSE:
                            print("\nFilling missing entry: ", next_entry, f" for field '{field}'")
                        next_entry[field] = current[field]
                        next_entry['rowspan'][field] = 1
                        if VERBOSE:
                            print("Filled to:", next_entry)

def _clean_db(capitals: List[Dict[str, Optional[str]]]) -> List[Dict[str, Optional[str]]]:
    """Clean the data by performing text replacements and other cleanup tasks."""
    reference_pattern = re.compile(r'\[\d+\]')
    space_before_parenthesis = re.compile(r'(?<!\s)\(') 
    space_after_punctuation = re.compile(r'([:.,])(?=\S)')
    for entry in capitals:
        for key, value in entry.items():
            if isinstance(value, str):
                value = reference_pattern.sub("", value)
                value = space_before_parenthesis.sub(" (", value)
                value = space_after_punctuation.sub(r'\1 ', value)  
                entry[key] = value.replace("de facto", "de facto - unofficial")  
                print("Cleaned entry: ", entry[key])

    capitals = _remove_rowspan(capitals)  
    return capitals

def clean_and_fill_db(capitals: List[Dict[str, Optional[str]]]) -> List[Dict[str, Optional[str]]]:
    """Clean and fill the DB of capitals with processed data."""
    _fill_db(capitals)   
    return _clean_db(capitals)

def push_capitals(capitals: List[Dict[str, Optional[str]]]) -> None:
    for capital_data in capitals:
        capital = capital_data.get("capital")  
        country = capital_data.get("country")
        continent = capital_data.get("continent")
        note = capital_data.get("note")

        data = {
            "Country": {"title": [{"text": {"content": country if country else ""}}]},  
            "Capital": {"rich_text": [{"text": {"content": capital if capital else ""}}]},
            "Continent": {"rich_text": [{"text": {"content": continent if continent else ""}}]},
            "Note": {"rich_text": [{"text": {"content": note if note else ""}}]},
        }

        create_page(data)