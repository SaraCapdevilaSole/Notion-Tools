import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN") or input("Please enter your Notion Integration Token (NOTION_TOKEN): ")
DATABASE_ID = os.getenv("DATABASE_ID") or input("Please enter your Notion Database ID (DATABASE_ID): ")

VERBOSE = True # prints duplicates

# First property name and type
NAME_TITLE = 'Name'
NAME_TYPE = 'TEXT' # other types not implemented

ENDPOINT = "https://api.notion.com/v1"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

DATE_TEMPLATE = lambda data_start, data_end=None: {"start": data_start, "end": data_end}


