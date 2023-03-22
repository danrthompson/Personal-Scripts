# read json file into a dict
import os

import json
import requests
import sys
import os
import re

import typing as T


URL = "https://api.track.toggl.com/api/v9/workspaces/397836/tags"
AUTH = (os.environ.get("TOGGL_API_KEY"), "api_token")
HEADERS = {"Content-Type": "application/json"}


tags_to_keep = ["useful", "planned", "worthwhile", "excessive", "still_in_bedroom_dumb"]
tags_to_keep.extend([f"{tag}_not" for tag in tags_to_keep])


# read json file into a dict
def read_json_file(filename) -> dict:
    with open(filename, "r") as f:
        return json.load(f)


ds = read_json_file("timery_tag_durations.json")
td = {d["Tag"]: (d["Duration"] / 60 / 60) for d in ds["Out"]}


def get_tags_less_than_n_hours_gt_o(n, o=-1):
    return [k for k, v in td.items() if v <= n and v > o]


# # make a request using python requests, and specify username and password


def get_toggl_tags():
    response = requests.get(URL, auth=AUTH, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to get tags")
        return []


def delete_toggl_tags(tags):
    tags = set(tags)
    data = get_toggl_tags()
    for d in data:
        if d["name"] in tags:
            print(f"Deleting {d['name']} with id {d['id']}")
            response = requests.delete(
                URL + "/" + str(d["id"]), auth=AUTH, headers=HEADERS
            )
            if response.status_code == 200:
                print("Deleted")
            else:
                print("Failed to delete")


def rename_toggl_tag(old_names_to_new_names: T.Dict[str, str]):
    data = get_toggl_tags()
    for d in data:
        if d["name"] in old_names_to_new_names:
            print(f"Renaming {d['name']} with id {d['id']}")
            new_name = old_names_to_new_names[d["name"]]
            response = requests.put(
                URL + "/" + str(d["id"]),
                auth=AUTH,
                headers=HEADERS,
                json={"name": new_name},
            )
            if response.status_code == 200:
                print("Renamed")
            else:
                print("Failed to rename")


def generate_old_to_new_tag_names():
    tags = get_toggl_tags()
    tags = [t["name"] for t in tags]
    old_to_new = {}
    for tag in tags:
        if tag not in tags_to_keep:
            old_to_new[tag] = f"Z_OLD_{tag}"

    return old_to_new


# curl  https://api.track.toggl.com/api/v9/workspaces/{workspace_id}/tags \
#   -H "Content-Type: application/json" \
#   -u <email>:<password>
