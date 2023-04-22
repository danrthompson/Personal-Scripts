#!/bin/zsh

tooling_mins=$(cat '/Users/danthompson/Code/Scripts/CLI/toggl textbar/data/opt_tooling_time_today.txt')
work_mins=$(cat '/Users/danthompson/Code/Scripts/CLI/toggl textbar/data/total_work_time_today.txt')

# get ratio of work time to tooling time
ratio=$(( (work_mins*100)/(work_mins+tooling_mins) ))

echo "$ratio"