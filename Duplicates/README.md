# Duplicate Removal Tool for Notion API

This tool helps to identify and remove duplicate entries from your Notion database by interacting with Notion's API.

## Setup Instructions

Follow these steps to configure and run the tool:

### 1. Create a Notion Integration
   - Go to [Notion Integrations](https://www.notion.so/my-integrations) and create a new integration.
   - You will receive a `NOTION_TOKEN`, which will be used for authenticating API requests.

### 2. Connect Your Notion Database
   - Open your Notion database (ensure it's set as a full-page database).
   - Share the database with your integration using the top right-hand-side three dots and clicking Connections.
   - Retrieve your `DATABASE_ID`:
     1. Click **Share** on the top right of your database.
     2. Copy the URL of the database. The `DATABASE_ID` will be the long alphanumeric string between the workspace name and the `?v=` part of the URL.  
     Example:  
     ```
     https://www.notion.so/workspace_name/DATABASE_ID?v=other_ids
     ```

### 3. Configure Your Environment
   - Add your `NOTION_TOKEN` and `DATABASE_ID` to the `config.py` file:
     ```python
     # config.py
     NOTION_TOKEN = 'your_notion_token'
     DATABASE_ID = 'your_database_id'
     ```

### 4. Run the Tool
   - Once your configuration is complete, you can run ```main.py``` to scan for and remove duplicate entries in your Notion database.

## Resources and References
For more information about using the Notion API with Python, check out this guide:  
[Python Engineer - Working with Notion API](https://www.python-engineer.com/posts/notion-api-python/)# Notion-Tools