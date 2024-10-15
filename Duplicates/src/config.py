NOTION_TOKEN = ""
DATABASE_ID = "" 

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


