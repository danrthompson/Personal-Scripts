import yaml
import os

TAGS_FILE = "tags.txt"
YAML_FILE = "tags.yaml"

STATUSES = ["unprocessed", "maybe", "yes", "no"]


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


def process_tags(tags):
    data = load_yaml()
    unprocessed_tags = [tag for tag in tags if tag not in data]

    for tag in unprocessed_tags:
        while True:
            print(f"Tag: {tag}")
            print(
                "Options: [Y]es, [M]aybe, [N]o, [U]ndo, [F-Q] Abort and reset all to unprocessed, [Q]uit"
            )
            choice = input("Your choice: ").strip().lower()

            if choice == "y":
                data[tag] = "yes"
                break
            elif choice == "m":
                data[tag] = "maybe"
                break
            elif choice == "n":
                data[tag] = "no"
                break
            elif choice == "u":
                if tag in data:
                    del data[tag]
                break
            elif choice == "f-q":
                data = {tag: "unprocessed" for tag in tags}
                break
            elif choice == "q":
                save_yaml(data)
                print("Exiting...")
                return

    save_yaml(data)

    for status in STATUSES[1:]:
        status_tags = [tag for tag, value in data.items() if value == status]
        for tag in status_tags:
            while True:
                print(f"Tag: {tag} (Status: {status.capitalize()})")
                print(
                    "Options: [Y]es, [M]aybe, [N]o, [U]ndo, [F-Q] Abort and reset all to unprocessed, [Q]uit"
                )
                choice = input("Your choice: ").strip().lower()

                if choice == "y":
                    data[tag] = "yes"
                    break
                elif choice == "m":
                    data[tag] = "maybe"
                    break
                elif choice == "n":
                    data[tag] = "no"
                    break
                elif choice == "u":
                    if tag in data:
                        del data[tag]
                    break
                elif choice == "f-q":
                    data = {tag: "unprocessed" for tag in tags}
                    break
                elif choice == "q":
                    save_yaml(data)
                    print("Exiting...")
                    return

    save_yaml(data)
    print("All tags processed and saved.")

    yes_tags = [tag for tag, value in data.items() if value == "yes"]
    no_tags = [tag for tag, value in data.items() if value == "no"]
    print("\nYes Tags:")
    print(yes_tags)
    print("\nNo Tags:")
    print(no_tags)


tags = load_tags()
process_tags(tags)
