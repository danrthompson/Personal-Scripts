import os
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Notion client
NOTION_KEY = os.getenv("NOTION_API_KEY")
if not NOTION_KEY:
    logger.error("NOTION_KEY environment variable is not set.")
    exit(1)

# For debugging, print the API key (remove after verifying)
print(f"Notion API Key: {NOTION_KEY}")

headers = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def get_all_databases():
    url = "https://api.notion.com/v1/search"
    data = {"filter": {"property": "object", "value": "database"}}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(
            f"Failed to retrieve databases: {response.status_code}, {response.text}"
        )
        return []

    return response.json().get("results", [])


def get_pages_in_database(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        logger.error(
            f"Failed to retrieve pages for database {database_id}: {response.status_code}, {response.text}"
        )
        return []

    return response.json().get("results", [])


database_info = []

# Retrieve all databases
databases = get_all_databases()
if not databases:
    logger.error("No databases found or failed to retrieve databases.")
    exit(1)

# Retrieve each database and collect information
for db in databases:
    db_id = db["id"]
    db_name = db["title"][0]["text"]["content"] if db["title"] else "Untitled"

    # Retrieve all pages in the database
    pages = get_pages_in_database(db_id)

    # Get last edited time and count of pages
    if pages:
        last_edited_time = max(page["last_edited_time"] for page in pages)
        page_count = len(pages)
    else:
        last_edited_time = "N/A"
        page_count = 0

    database_info.append(
        {"name": db_name, "rows": page_count, "last_edited_time": last_edited_time}
    )

# Sort by the most recent row added
sorted_by_recent = sorted(
    database_info, key=lambda x: x["last_edited_time"], reverse=True
)

# Sort by the number of rows
sorted_by_rows = sorted(database_info, key=lambda x: x["rows"], reverse=True)

# Print the sorted lists
print("Databases sorted by most recent row added:")
for db in sorted_by_recent:
    print(
        f"Name: {db['name']}, Rows: {db['rows']}, Last Edited Time: {db['last_edited_time']}"
    )

print("\nDatabases sorted by number of rows:")
for db in sorted_by_rows:
    print(
        f"Name: {db['name']}, Rows: {db['rows']}, Last Edited Time: {db['last_edited_time']}"
    )
