import os

import pandas as pd
from toggl.TogglPy import Toggl

WORKSPACE_ID = 397836

toggl = Toggl()


if api_key := os.environ.get("TOGGL_API_KEY"):
    toggl.setAPIKey(api_key)
else:
    print("TOGGL_API_KEY environment variable not set")
    exit(1)

# Get all projects
projects = toggl.getWorkspaceProjects(WORKSPACE_ID)

projects_df = pd.DataFrame(projects)

clients = toggl.getClients()

clients_df = pd.DataFrame(clients)

projects_df.join()in(clients_df, on="cid", how="left", )
