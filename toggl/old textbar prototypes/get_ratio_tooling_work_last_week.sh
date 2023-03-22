#!/bin/zsh

tooling_mins=$(cat ~/Code/Scripts/opt_tooling_time_last_week.txt)
work_mins=$(cat ~/Code/Scripts/total_work_time_last_week.txt)

ratio=$(( (work_mins*100)/(work_mins+tooling_mins) ))

echo "$ratio"
