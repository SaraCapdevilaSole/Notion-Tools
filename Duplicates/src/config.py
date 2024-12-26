import os
import logging

# Get environment variables
NOTION_TOKEN: str = os.getenv("NOTION_TOKEN") or input("Please enter your Notion Integration Token (NOTION_TOKEN): ")
DATABASE_ID: str = os.getenv("DATABASE_ID") or input("Please enter your Notion Database ID (DATABASE_ID): ")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set verbose flag
VERBOSE: bool = True # prints duplicates

