# URL (World Capitals) Scraper for Notion API

This tool automates the process of fetching world capitals from [Wikipedia](https://en.wikipedia.org/wiki/List_of_national_capitals) and adding them to your Notion database.

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
   - You can configure your `NOTION_TOKEN` and `DATABASE_ID` by either:
   1. **Environment Variables**: Set environment variables in your terminal.
      ```bash
      # For Windows
      set NOTION_TOKEN=your_notion_token
      
      # For Mac/Linux
      export NOTION_TOKEN=your_notion_token
      ```
   2. **`config.py` File**: Users can hardcode the values in the `config.py` file.
      e.g., 
      ```python
      NOTION_TOKEN = 'your_notion_token'
      DATABASE_ID = 'your_database_id'
      ```
   3. **Prompt**: If the values are not found in the environment or `config.py`, the script will prompt the user.
     

### 4. Run the Tool
    - Once your configuration is complete, run the script to fetch, parse, and add entries to your Notion database:
     ```bash
     python find_capitals.py
     ```

## Resources and References
For more information about using the Notion API with Python, check out this guide:  
[Python Engineer - Working with Notion API](https://www.python-engineer.com/posts/notion-api-python/)# Notion-Tools
