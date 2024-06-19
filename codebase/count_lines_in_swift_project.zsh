find . -type f -name '*.swift' -exec wc -l {} + | awk '
{
    # Skip the total line
    if ($2 == "total") {
        next;
    }
    # Reset file_path
    file_path = "";
    # Concatenate all fields starting from the second to construct the file path
    for (i = 2; i <= NF; i++) {
        file_path = (file_path ? file_path " " : "") $i;
    }
    # Trim leading whitespace from file_path
    gsub(/^ +/, "", file_path);
    # Print the file path and the line count
    print file_path ": " $1;
    # Accumulate the total line count
    total += $1;
}
END { print "Total lines of code: " total }'
