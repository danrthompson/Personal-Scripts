import yaml
import os

TAGS_FILE = "tags.txt"
YAML_FILE = "tags.yaml"
CATEGORIES_KEY = "categories"


def load_tags():
    if not os.path.exists(TAGS_FILE):
        print(f"Tags file '{TAGS_FILE}' does not exist.")
        return []

    with open(TAGS_FILE, "r") as file:
        tags = file.read().splitlines()
    return tags


def load_yaml():
    if not os.path.exists(YAML_FILE):
        return {}

    with open(YAML_FILE, "r") as file:
        data = yaml.safe_load(file)
    return data


def save_yaml(data):
    with open(YAML_FILE, "w") as file:
        yaml.dump(data, file)


def get_categories():
    if os.path.exists(YAML_FILE):
        data = load_yaml()
        if CATEGORIES_KEY in data:
            return data[CATEGORIES_KEY]

    categories = input("Enter the categories separated by commas: ").strip().split(",")
    categories = [category.strip() for category in categories]
    return categories


def get_choice(categories):
    print("\nOptions:")
    print("  [U]ndecided (Come Back Later)")
    for index, category in enumerate(categories):
        print(f"  [{index + 1}] {category}")
    print("  [Q]uit and Save")
    print("  [Q-S]uit without Saving")
    print("  [D]isplay Results")
    choice = input("Your choice: ").strip().lower()
    return choice


def process_tags(tags, categories):
    data = load_yaml()

    if not data:
        data = {tag: None for tag in tags}
        data[CATEGORIES_KEY] = categories
        save_yaml(data)

    while True:
        unprocessed_tags = [tag for tag, value in data.items() if value is None]
        if not unprocessed_tags:
            break

        for tag in unprocessed_tags:
            print(f"\nTag: {tag}")
            choice = get_choice(categories)

            if choice == "u":
                data[tag] = None
            elif choice.isdigit() and int(choice) in range(1, len(categories) + 1):
                data[tag] = categories[int(choice) - 1]
            elif choice == "q":
                save_yaml(data)
                print("Exiting...")
                return
            elif choice == "q-s":
                print("Exiting without saving...")
                return
            elif choice == "d":
                display_results(data, categories)
            else:
                print("Invalid choice. Please try again.")

            save_yaml(data)

    print("All tags processed and saved.")
    display_results(data, categories)


def display_results(data, categories):
    results = {}
    for category in categories:
        results[category] = [tag for tag, value in data.items() if value == category]

    print("\nResults So Far:")
    for category, tags in results.items():
        print(f"\n{category.capitalize()} Tags:")
        print(tags)


tags = load_tags()
categories = get_categories()
process_tags(tags, categories)
