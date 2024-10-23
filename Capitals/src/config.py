import os

# Notion config
NOTION_TOKEN = os.getenv("NOTION_TOKEN") or input("Please enter your Notion Integration Token (NOTION_TOKEN): ")
DATABASE_ID = os.getenv("DATABASE_ID") or input("Please enter your Notion Database ID (DATABASE_ID): ")

ENDPOINT = "https://api.notion.com/v1"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Capitals (Wikipedia) information
URL = 'https://en.wikipedia.org/wiki/List_of_national_capitals'

CONTINENTS = ['Asia', 'Africa', 'North America', 'South America', 'Europe', 'Oceania', 'Antarctica']

DB_TEMPLATE = {
        'capital': None,
        'country': None,
        'continent': None,
        'note': None,
    }

DB_TEMPLATE['rowspan'] = {k: 1 for k in DB_TEMPLATE}

VERBOSE = True