# %%
from collections import defaultdict

# %%
uncategorized = [
    "10-happier",
    "101-design-methods",
    "a-mind-for-numbers",
    "algorithms-to-live-by",
    "antifragile",
    "atomic-habits",
    "behave",
    "breath",
    "building-a-second-brain",
    "cognitive-behavior-therapy-basics-and-beyond",
    "deep-work",
    "designing-the-mind",
    "designing-your-life",
    "dopamine-detox",
    "dopamine-nation",
    "driven-to-distraction",
    "effortless",
    "emotional-intelligence",
    "emotional-intelligence-2-0",
    "essentialism",
    "exponential-organizations",
    "flow",
    "focus",
    "fooled-by-randomness",
    "getting-things-done",
    "getting-to-yes",
    "goals",
    "guns-germs-and-steel",
    "homo-deus",
    "how-democracies-die",
    "how-to-be-an-antiracist",
    "how-to-become-a-straight-a-student",
    "how-to-take-smart-notes",
    "how-to-talk-to-anyone",
    "how-to-win-friends-and-influence-people",
    "hyperfocus",
    "i-will-teach-you-to-be-rich",
    "ikigai",
    "influence",
    "lifespan",
    "make-it-stick",
    "meditations",
    "mindfulness-in-plain-english",
    "never-split-the-difference",
    "nudge",
    "peak",
    "principles-life-and-work",
    "procrastination",
    "psycho-cybernetics",
    "quiet-the-power-of-introverts",
    "sapiens",
    "scrum",
    "smarter-faster-better",
    "spark",
    "stop-overthinking",
    "super-thinking-the-big-book-of-mental-models",
    "superforecasting",
    "surely-youre-joking-mr-feynman",
    "surrounded-by-idiots",
    "team-topologies",
    "the-4-hour-body",
    "the-4-hour-workweek",
    "the-5-second-rule",
    "the-80-20-principle",
    "the-art-of-thinking-clearly",
    "the-beginning-of-infinity",
    "the-black-swan",
    "the-brain-that-changes-itself",
    "the-coddling-of-the-american-mind",
    "the-emperor-of-all-maladies",
    "the-extended-mind",
    "the-four-tendencies",
    "the-gene",
    "the-goal-a-process-of-ongoing-improvement",
    "the-great-mental-models-volume-1",
    "the-great-mental-models-volume-2",
    "the-great-mental-models-volume-3",
    "the-highly-sensitive-person",
    "the-innovator-s-dilemma",
    "the-master-guides-focus",
    "the-motivation-myth",
    "the-now-habit",
    "the-obesity-code",
    "the-only-study-guide-youll-ever-need",
    "the-organized-mind",
    "the-power-of-habit",
    "the-productivity-project",
    "the-righteous-mind",
    "the-road-to-character",
    "the-subtle-art-of-not-giving-a-f-ck",
    "the-willpower-instinct",
    "thinking-fast-and-slow",
    "thinking-in-systems",
    "tiny-habits",
    "tools-of-titans",
    "triggers",
    "ultralearning",
    "unwinding-anxiety",
    "why-zebras-dont-get-ulcers",
    "zero-to-one",
]

# %%
# index = 0
# uncategorized = uncategorized[index:]


# %%
def process_books(
    uncategorized,
    book_categories=None,
    use_later: bool = False,
    use_index: bool = False,
):
    if book_categories is None:
        book_categories = defaultdict(list)

    index = book_categories["index"][-1] if book_categories["index"] else 0

    if use_index:
        uncategorized = uncategorized[index:]

    if use_later:
        uncategorized = book_categories["later"] + uncategorized

    abort = False
    for book in uncategorized:
        if abort:
            break
        print(book)
        success: bool = False
        while not success:
            success = True
            char = input()
            if char == "y":
                book_categories["read_liked"].append(book)

            elif char == "h":
                book_categories["heard_good"].append(book)

            elif char == "d":
                book_categories["didnt_like"].append(book)

            elif char == "r":
                book_categories["havent_read"].append(book)

            elif char == "u":
                book_categories["unsure"].append(book)

            elif char == "l":
                book_categories["later"].append(book)

            elif char == "q":
                abort = True
                break

            elif char == "?":
                print(
                    "y: read and liked,h: heard good things\nd: didn't like, r: haven't read\nu: unsure, l: later, q: quit"
                )
                success = False

            else:
                print("invalid")
                success = False
        if success:
            index += 1

    book_categories["index"].append(index)

    return book_categories, index


# %%
book_categories = None
# %%
# book_categories, index = process_books(uncategorized)
book_categories, index = process_books(
    uncategorized, book_categories, use_index=True, use_later=True
)

# %%

# %%
for key, value in book_categories.items():
    print(f"{key}: {len(value)}\n{value}\n\n")


# Read and liked:

# Haven't read, but it at least seemed interesting at first glace:

# Uncategorized:

# %%
