# %%
import os

from todoist_api_python.api import TodoistAPI
from pprint import pprint

# %%
api = TodoistAPI(os.environ.get("TODOIST_API_KEY"))

# %%
labels = api.get_labels()
pprint(labels)

# %%
