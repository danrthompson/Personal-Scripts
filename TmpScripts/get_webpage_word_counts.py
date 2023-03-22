# get the number of words on a webpage
# Usage: python get_webpage_word_counts.py http://www.google.com

# %%
import os

import math
import pandas as pd
import requests
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment


# %%
time_taken_chp_6 = 115
time_taken_chp_7 = 170
time_taken_chp_8 = 92

# %%
def get_webpage_word_counts(url):
    r = requests.get(url)
    s = BeautifulSoup(r.content, "html.parser")
    for sc in s(["script", "style"]):
        sc.extract()
    for cm in s.find_all(string=lambda t: isinstance(t, Comment)):
        cm.extract()
    txt = s.find_all(text=True)
    out = []
    for t in txt:
        out += t.replace("\n", "").replace("\r", "").split(" ")
    out = [t for t in out if t]
    return len(out)


def get_summaries_from_toggl(start_date, end_date, project_ids):
    return requests.post(
        "https://api.track.toggl.com/reports/api/v3/workspace/397836/summary/time_entries",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {"end_date": end_date, "start_date": start_date, "project_ids": project_ids}
        ),
        auth=(os.environ.get("TOGGL_API_KEY"), "api_token"),
    ).json()


# %%
def print_time(label, mins):
    mins_rounded = round(mins, 2)
    hours = math.floor(mins / 60)
    mins = round(mins % 60)
    print(f"{label}: {hours}:{mins:02d} ({mins_rounded} minutes)")


# %%
# get_webpage_word_counts("https://wesmckinney.com/book/preface.html")
# %%
# write a function to get all the pages from the table of contents


def get_all_pages(url):
    r = requests.get(url)
    s = BeautifulSoup(r.content, "html.parser")
    links = s.find_all("a")
    out = []
    for link in links:
        if link.get("href"):
            # the link contains a span with class "chapter-title"
            if link.find("span", {"class": "chapter-title"}):
                # add the absolute link path (not the relative path) to the output
                out.append(
                    (
                        "https://wesmckinney.com/book" + link.get("href").lstrip("."),
                        link.find("span", {"class": "chapter-number"}).text,
                        link.find("span", {"class": "chapter-title"}).text,
                    )
                )
    return out


# %%
# get pages
# pages = get_all_pages("https://wesmckinney.com/book/preface.html")
# pages = pages[:-1]
# print(pages)

# %%
# get the word counts for each page
# word_counts = []
# for page in pages:
#     word_counts.append((page[1], get_webpage_word_counts(page[0])))
# word_counts

# %%
# store the word counts as a variable
word_counts = [
    ("1", 5532),
    ("2", 8381),
    ("3", 11518),
    ("4", 13122),
    ("5", 13401),
    ("6", 8648),
    ("7", 12433),
    ("8", 9555),
    ("9", 6464),
    ("10", 10242),
    ("11", 14783),
    ("12", 5683),
    ("13", 11937),
    ("A", 11387),
    ("B", 8737),
]

# %%
all_times_taken = [
    time_taken_chp_6,
    time_taken_chp_7,
    time_taken_chp_8,
]
total_time_taken = sum(all_times_taken)
not_done_counts = word_counts[8:]
total = sum(map(lambda x: x[1], word_counts))
chp_6, chp_7, chp_8, chp_9 = word_counts[5:9]
chp_6_pct = chp_6[1] / total
chp_7_pct = chp_7[1] / total
chp_8_pct = chp_8[1] / total
chp_9_pct = chp_9[1] / total
done_tracked_percentages = [
    chp_6_pct,
    chp_7_pct,
    chp_8_pct,
]
done_tracked_total_pct = sum(done_tracked_percentages)
not_done = sum(map(lambda x: x[1], not_done_counts))
not_done_pct = not_done / total
done_pct = 1 - not_done_pct
mins_remaining_from_6 = not_done_pct * (time_taken_chp_6 / chp_6_pct)
mins_remaining_from_7 = not_done_pct * (time_taken_chp_7 / chp_7_pct)
mins_remaining_from_8 = not_done_pct * (time_taken_chp_8 / chp_8_pct)
mins_remaining_from_7_8 = not_done_pct * (
    (time_taken_chp_8 + time_taken_chp_7) / (chp_8_pct + chp_7_pct)
)
mins_total_from_all = total_time_taken / done_tracked_total_pct
mins_remaining_from_all = not_done_pct * mins_total_from_all
mins_for_chp_9_from_all = chp_9_pct * mins_total_from_all
mins_for_chp_9_from_7 = chp_9_pct * (time_taken_chp_7 / chp_7_pct)
mins_for_chp_9_from_8 = chp_9_pct * (time_taken_chp_8 / chp_8_pct)
mins_for_chp_9_from_7_8 = chp_9_pct * (
    (time_taken_chp_8 + time_taken_chp_7) / (chp_8_pct + chp_7_pct)
)

# %%
print(f"Done: {done_pct}")
print(f"Not Done: {not_done_pct}")
# %%
print_time("Estimated time remaining from 6", mins_remaining_from_6)
print_time("Estimated time remaining from 7:", mins_remaining_from_7)
print_time("Estimated time remaining from 8:", mins_remaining_from_8)
print_time("Estimated time remaining from 7+8:", mins_remaining_from_7_8)
print_time("Estimated time remaining from all:", mins_remaining_from_all)
print_time("Estimated time for chapter 9 from all:", mins_for_chp_9_from_all)
print_time("Estimated time for chapter 9 from 8:", mins_for_chp_9_from_8)
print_time("Estimated time for chapter 9 from 7:", mins_for_chp_9_from_7)
print_time("Estimated time for chapter 9 from 7+8:", mins_for_chp_9_from_7_8)
# %%
# %%
# make word_count into a dataframe
df = pd.DataFrame(word_counts, columns=["chapter", "word_count"])
df
# %%
