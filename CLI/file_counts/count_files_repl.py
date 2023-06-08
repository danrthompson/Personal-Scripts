import os

# Memoization dictionary
memo = {}


def count_files(dirpath):
    if dirpath in memo:
        return memo[dirpath]

    count = sum(len(files) for _, _, files in os.walk(dirpath))
    memo[dirpath] = count

    return count


def interactive_explore(dirpath):
    while True:
        print(f"Current Directory: {dirpath}")  # Display current directory
        dir_items = sorted(
            [
                os.path.join(dirpath, item)
                for item in os.listdir(dirpath)
                if os.path.isdir(os.path.join(dirpath, item))
            ],
            key=lambda x: count_files(x),  # sort by number of files
        )
        dir_counts = {item: count_files(item) for item in dir_items}

        for i, item in enumerate(dir_items, start=1):
            print(f"{i}. {os.path.basename(item)} - {dir_counts[item]} files")
        print("U. Go up a level")
        print("Q. Quit")

        choice = input(
            "Select a directory to explore, U to go up a level, or Q to quit: "
        )
        if choice.upper() == "Q":
            break
        elif choice.upper() == "U":
            return  # Return to the caller
        elif choice.isdigit() and 1 <= int(choice) <= len(dir_items):
            interactive_explore(dir_items[int(choice) - 1])
        else:
            print("Invalid choice, try again.\n")
