import requests
from base64 import b64encode

# Replace these with your actual API token and workspace ID
API_TOKEN = b"83023fc45cedcf56f11bb9d9c34a3093:api_token"
WORKSPACE_ID = '397836'

# Toggl API URL for tags
TAGS_URL = f'https://api.track.toggl.com/api/v9/workspaces/{WORKSPACE_ID}/tags'

# Set up authorization header
auth_header = {'content-type': 'application/json', 'Authorization' : 'Basic %s' %  b64encode(API_TOKEN).decode("ascii")}

def get_tags():
    """Fetch all tags in the workspace."""
    response = requests.get(TAGS_URL, headers=auth_header)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch tags:", response)
        return []

def update_tag_name(tag):
    """Update the tag name by prefixing it with 'zzz_'."""
    tag_id = tag['id']
    new_name = f'zzz_{tag["name"]}'
    update_url = f'{TAGS_URL}/{tag_id}'
    data = {'name': new_name}
    response = requests.put(update_url, json=data, headers=auth_header)
    if response.status_code == 200:
        print(f'Tag {tag["name"]} updated to {new_name}')
    else:
        print(f'Failed to update tag {tag["name"]}:', response.text)



def main():

    tags = get_tags()
    for tag in tags:
        print(tag['name'])
        # # Skip tags already prefixed with 'zzz_'
        if not tag['name'].startswith('zzz_'):
            update_tag_name(tag)

if __name__ == '__main__':
    main()
