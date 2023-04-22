#!/bin/zsh

total_mins_last_week=$(cat /Users/danthompson/Code/Scripts/CLI/toggl textbar/data/total_work_time_last_week.txt)

hours_last_week=$((total_mins_last_week/60))
mod_mins_last_week=$((total_mins_last_week%60))
# pad with leading zero if needed
[[ $mod_mins_last_week -lt 10 ]] && mod_mins_last_week="0$mod_mins_last_week"

echo "$hours_last_week:$mod_mins_last_week"