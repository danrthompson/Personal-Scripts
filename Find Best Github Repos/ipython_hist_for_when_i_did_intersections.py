import json


f1 = "first_small_total.json"
f2 = "large_small_total.json"
f3 = "large_total.json"
f4 = "old_small_total.json"
f5 = "small_cli_or_tool_all.json"
file_names = [f1, f2, f3, f4, f5]


def generate_key_to_item_dict(this_dict, key):
    return {item[key]: item for item in this_dict}


def get_all_ints(file_names, key, keep_indices=False):
    dict_list = []
    for file_name in file_names:
        with open(file_name) as f:
            this_dict = json.load(f)
            dict_list.append(this_dict)

    int_list = []
    file_len = len(file_names)
    for i in range(file_len):
        for j in range(i + 1, file_len):
            this_intersection = get_int(dict_list[i], dict_list[j], key, i, j)
            int_list.append((i, j, this_intersection))

    sorted_int_list = sorted(int_list, key=lambda x: len(x[2]), reverse=True)
    sorted_int_list = [item for item in sorted_int_list if item]

    return sorted_int_list if keep_indices else [tup[2] for tup in sorted_int_list]


def find_common_elements(int_list, key, min_num_elements=2):
    set_list = []
    for il in int_list:
        urls = [item[key] for item in il]
        url_set = set(urls)
        set_list.append(url_set)

    all_items = get_all_unique_values(int_list)
    key_to_items = generate_key_to_item_dict(all_items, key)

    item_count: dict[str, int] = {}

    for this_set in set_list:
        for item in this_set:
            item_count[item] = item_count.get(item, 0) + 1

    # filter out items that don't appear in at least min_num_elements lists
    min_items: dict[str, int] = {
        key: value for key, value in item_count.items() if value >= min_num_elements
    }
    min_items = dict(sorted(min_items.items(), key=lambda x: x[1], reverse=True))

    ret_list: list[tuple[dict, int]] = [
        (key_to_items[this_key], this_val) for this_key, this_val in min_items.items()
    ]
    return ret_list


def get_int(d1, d2, key, i=None, j=None):
    d1q = generate_key_to_item_dict(d1, key)
    d2q = generate_key_to_item_dict(d2, key)
    this_int = [value for key, value in d1q.items() if key in d2q]
    print(
        f"{f'i: {i}. ' if i else ''}{f'j: {j}. ' if j else ''}f1: {len(d1)}. f2: {len(d2)}. Int: {len(this_int)}"
    )
    return sorted(this_int, key=len, reverse=True)


def get_all_unique_values(int_list):
    all_items = [subval for val in int_list for subval in val]
    urls_so_far = set([])
    items_to_keep = []
    for item in all_items:
        if item["id"] in urls_so_far:
            continue
        urls_so_far.add(item["id"])
        items_to_keep.append(item)

    return items_to_keep


int_list = get_all_ints(file_names, "url")
int_list_len = len(int_list)


all_items = get_all_unique_values(int_list)
len(all_items)
sum([1 for item in all_items if item["pushedAt"] > "2023"])
sum([1 for item in all_items if item["stargazersCount"] > 0])
sum([item["stargazersCount"] for item in all_items])
sum([item["stargazersCount"] for item in all_items]) / len(all_items)

ce_items = find_common_elements(int_list, "url")
len(ce_items)
sum([item["stargazersCount"] for item in ce_items]) / len(ce_items)
