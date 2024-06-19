# sample search written into a file
gh search repos "gpt code in:name in:description stars:>=1 pushed:>2023-01-01" -L 1000 --json "id,name,url,pushedAt,stargazersCount" > small_gpt_code_bm.json
# note that if it returns too many we might need to sort a couple additional ways and combine
gh search repos "gpt code in:name in:description stars:>=1 pushed:>2023-01-01" -L 1000 --json "id,name,url,pushedAt,stargazersCount" --sort "updated" > small_gpt_code_updated.json
gh search repos "gpt code in:name in:description stars:>=1 pushed:>2023-01-01" -L 1000 --json "id,name,url,pushedAt,stargazersCount" --sort "stars" > small_gpt_code_stars.json

# now combine with jq
jq -s 'add | unique_by(.id)' small_gpt_code_bm.json small_gpt_code_updated.json > total2.json
mv total2.json total.json
jq -s 'add | unique_by(.id)' total.json small_gpt_code_stars.json > total2.json
mv total2.json small_gpt_code_all.json

# TODO: This should all be done in Python so I can make functions

# Some notes: we want some small queries to ensure that those repos are covering what we actually want. Search for the main keywords, only in name and description. Like ones above
# You can reduce numbers further by adding keywords, adding filters on stars or when pushed, etc
# If two searches use the same keyword meaning, but with different words, those lists should be combined

# After that, we want to maybe search a bit wider. We are going to search within the readme to do this. This is our chance to search for more specific keywords. Some repos might match the small queries but could be ruled out with the additional keywords.
# The tricky part though is that usually if you search in the readme, you get a lot of false positives. And conversely, if we didn't include the readme, we would not get any results just from the name or description with more specific keywords.
# So my approach is to do a more general search on name and description and a more specific search on the readme. If we are doing multiple similar queries, combine them. Then we take the lists that result, and take the intersection. But usually we don't want to require that a repo is in every list (we may have a lot).
# So what I did last time, is I had 5 lists. I took the intersection of each pair, resulting in 10 lists. 3 were blank, so we were left with 7. Then I took the results that were in at least 2 of those lists.
# It's not clear this is the best approach. Integrating GPT would be really useful actually. But I think it's a good start.

# Get length of file jq
jq 'length' small_cli_or_tool_all.json

# Intersection can be done with jq but I just did it in Python

# One other useful json terminal tool, other than jq, is fx. Lets you use Python, but only takes in one file or input at a time unfortunately. Just occurred to me that you could make that work using a dictionary with the file names as keys and the json as values. But probably better to do it in Python.

# One other I saw was jello. Not sure if it can be done with that.