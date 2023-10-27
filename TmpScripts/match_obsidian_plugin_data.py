import csv
import difflib
from collections import OrderedDict


# Define file names
CSV_FILENAME = "plugins.csv"
LIST_FILENAME = "plugin_list.txt"
RESULTS_FILENAME = "matched_plugins.csv"


# Load the data from the CSV file
def load_csv_data(filename):
    """
    Load data from a CSV file and return a dictionary with plugin names as keys and rows as values.

    Args:
        filename (str): The name of the CSV file to load.

    Returns:
        dict: A dictionary with plugin names as keys and rows as values.
    """
    data = {}
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            plugin_name = row[
                0
            ].lower()  # Convert to lowercase for case-insensitive match
            data[plugin_name] = row
    return data


# Load the data from the list file
def load_list_data(filename):
    """
    Load data from a text file and return a list of plugin names.

    Args:
        filename (str): The name of the text file to load.

    Returns:
        list: A list of plugin names.
    """
    data: list[str] = []
    with open(filename, "r", encoding="utf-8") as file:
        data.extend(line.strip().lower() for line in file if not line.startswith("#"))
    return data


# Fuzzy match function
def fuzzy_match(plugin_name, plugin_dict):
    """
    Find the closest matches for a given plugin name in a dictionary of plugin names.

    Args:
        plugin_name (str): The name of the plugin to match.
        plugin_dict (dict): A dictionary with plugin names as keys and rows as values.

    Returns:
        list: A list of the closest matches for the given plugin name.
    """
    if closest_matches := difflib.get_close_matches(
        plugin_name, plugin_dict.keys(), n=2
    ):
        return closest_matches
    return []


# Load CSV and list data
csv_data = load_csv_data(CSV_FILENAME)
list_data = load_list_data(LIST_FILENAME)

# For keeping the results
results = OrderedDict()

# For keeping the ones to double-check
check = []

# Create a SequenceMatcher instance
seq_match = difflib.SequenceMatcher()

# Iterate through the list data and match with CSV data
for plugin in list_data:
    if plugin in csv_data:
        results[plugin] = csv_data[plugin]
    elif matches := fuzzy_match(plugin, csv_data):
        best_match = matches[0]
        results[plugin] = csv_data[best_match]
        # Check similarity scores
        seq_match.set_seqs(plugin, best_match)
        score_best = seq_match.ratio()
        if len(matches) > 1:
            seq_match.set_seqs(plugin, matches[1])
            # score_second = seq_match.ratio()
            # if (
            #     score_second >= 0. * score_best
            # ):  # if the second score is within 25% of the best score
            check.append((plugin, matches))
        results[plugin].append(best_match)
    else:
        check.append((plugin, matches))  # if no matches were found

# Save results to a file
with open(RESULTS_FILENAME, "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    for name, details in results.items():
        writer.writerow(details)

# Print the ones to double-check and their possible matches
print("Plugins to double-check: ")
for plugin, matches in check:
    print(f"Plugin: {plugin}, Matches: {matches}")
