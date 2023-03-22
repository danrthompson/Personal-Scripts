#%%
import os

import requests
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"


start_date = (datetime.now() - timedelta(days=20)).strftime(DATE_FORMAT)
end_date = datetime.now().strftime(DATE_FORMAT)
url = "https://api.track.toggl.com/api/v9/me/time_entries"
headers = {"Content-Type": "application/json"}
auth = (os.environ.get("TOGGL_API_KEY"), "api_token")
payload = {
    "start_date": start_date,
    "end_date": end_date,
}

response = requests.get(url, headers=headers, auth=auth, params=payload)
# %%
response
#%%
resp_json = response.json()
# %%
resp_json


# %%

sex_acts = [
    datetime.strptime(entry["start"], "%Y-%m-%dT%H:%M:%S%z")
    for entry in resp_json
    if "fun_ollie_success" in entry["tags"]
]

sex_act_days = list(map(lambda x: x.date(), sex_acts))

len(set(sex_act_days))

# %%
