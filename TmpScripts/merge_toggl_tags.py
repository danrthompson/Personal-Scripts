import requests
from datetime import datetime, timedelta, timezone

API_TOKEN = "83023fc45cedcf56f11bb9d9c34a3093"
AUTH = (API_TOKEN, "api_token")

# TAGS_TO_MERGE = [
#     "aa_work_type_programming",
#     "aa_work_type_idea_implementation",
#     "a_c_real_work",
#     "2_1_direct work",
# ]

# NEW_TAG = "b_work_task_direct"

# TAGS_TO_MERGE = [
#     "2_1_direct_work",
#     "a_c_real_work",
#     "aa_work_type_idea_implementation",
#     "aa_work_type_programming",
# ]
# NEW_TAG = "b_work_task_strategy_planning"
TAGS_TO_MERGE = [
    "2_2_strategy_prioritize_planning",
    "aa_work_planning_project",
    "2_6_meeting_general",
]
NEW_TAG = "b_work_task_strategy_planning"
# TAGS_TO_MERGE = [
#     "a_b_research",
#     "2_3_research",
#     "aa_work_type_research",
#     "a_d_learning",
#     "aa_work_type_course",
# ]
# NEW_TAG = "b_work_task_research"
TAGS_TO_MERGE = [
    "2_4_scheduling_timeboxing",
    "aa_work_planning_schedule",
    "2_5_clickup_review_organization",
]
NEW_TAG = "b_work_task_scheduling_task_mgmt"


TIME_ENTRIES_ENDPOINT = "https://api.track.toggl.com/api/v8/time_entries"
TAGS_ENDPOINT = "https://api.track.toggl.com/api/v8/tags"


def get_time_entries(start_date, end_date):
    # Ensure the datetime objects are timezone-aware
    start_date = start_date.replace(tzinfo=timezone.utc)
    end_date = end_date.replace(tzinfo=timezone.utc)

    # Manually formatting date to include colon in timezone
    start_date_str = (
        start_date.strftime("%Y-%m-%dT%H:%M:%S")
        + start_date.strftime("%z")[:3]
        + ":"
        + start_date.strftime("%z")[3:]
    )
    end_date_str = (
        end_date.strftime("%Y-%m-%dT%H:%M:%S")
        + end_date.strftime("%z")[:3]
        + ":"
        + end_date.strftime("%z")[3:]
    )

    params = {"start_date": start_date_str, "end_date": end_date_str}

    all_entries = []
    max_requests = 10  # Set a max number of requests to avoid infinite loop

    for _ in range(max_requests):
        response = requests.get(TIME_ENTRIES_ENDPOINT, auth=AUTH, params=params)

        # Debugging outputs:
        # print(f"Request URL: {response.url}")  # Print the URL being requested
        # print(f"Response Status: {response.status_code}")  # Print the status code
        # print(f"Response Body: {response.text}")  # Print the response body

        if response.status_code == 200:
            entries = response.json()
            all_entries.extend(entries)
            if len(entries) < 1000:
                break
            else:
                last_entry = entries[-1]
                # Ensure the correct datetime format while updating `start_date`
                start_date = datetime.fromisoformat(last_entry["start"]) + timedelta(
                    seconds=1
                )
                # Manually formatting date to include colon in timezone for the updated `start_date`
                params["start_date"] = (
                    start_date.strftime("%Y-%m-%dT%H:%M:%S")
                    + start_date.strftime("%z")[:3]
                    + ":"
                    + start_date.strftime("%z")[3:]
                )
        else:
            response.raise_for_status()

    return all_entries


def update_time_entry(time_entry_id, tags):
    payload = {"time_entry": {"tags": tags, "tag_action": "set"}}
    response = requests.put(
        f"{TIME_ENTRIES_ENDPOINT}/{time_entry_id}", auth=AUTH, json=payload
    )
    if response.status_code != 200:
        print(f"Failed to update time entry {time_entry_id}: {response.content}")


def merge_tags(start_date, end_date):
    time_entries = get_time_entries(start_date, end_date)
    for entry in time_entries:
        if "tags" in entry and any(tag in TAGS_TO_MERGE for tag in entry["tags"]):
            new_tags = [tag for tag in entry["tags"] if tag not in TAGS_TO_MERGE]
            new_tags.append(NEW_TAG)
            update_time_entry(entry["id"], new_tags)
            print(f"Updated time entry {entry['id']} with tags: {new_tags}")


if __name__ == "__main__":
    # Update entries for 2022
    # start_date_2022 = datetime(2022, 1, 1)
    # end_date_2022 = datetime(2022, 12, 31, 23, 59, 59)
    # merge_tags(start_date_2022, end_date_2022)

    # # Update entries for 2023
    start_date_2023 = datetime(2023, 3, 1)
    end_date_2023 = datetime(2023, 12, 31, 23, 59, 59)
    # end_date_2023 = datetime(2023, 4, 1)
    merge_tags(start_date_2023, end_date_2023)
