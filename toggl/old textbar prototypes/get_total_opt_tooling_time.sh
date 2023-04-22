#!/bin/zsh

# AI 186181594
# investments 187316243
# special work projects 188326563
# work planning 188079427
# work med prod 186193242
# excessive tooling 187944113
# tooling 186181587
# tracking 188328043
# prod 188539366

last_week=$(date -v-6d +%Y-%m-%d)
today=$(date +%Y-%m-%d)

# "group_ids":["integer"],"grouping":"string","include_time_entry_ids":"boolean""sub_grouping":"string"
summary_today=$(curl -s -X POST https://api.track.toggl.com/reports/api/v3/workspace/397836/summary/time_entries \
  -H "Content-Type: application/json" \
  -d "{\"end_date\":\"${today}\",\"start_date\":\"${today}\",\"project_ids\":[187944113,186181587,188328043]}" \
  -u ${TOGGL_API_KEY}:api_token |jq '[.groups | .[]|."sub_groups"|.[]|.seconds]|add')

summary_last_week=$(curl -s -X POST https://api.track.toggl.com/reports/api/v3/workspace/397836/summary/time_entries \
  -H "Content-Type: application/json" \
  -d "{\"end_date\":\"${today}\",\"start_date\":\"${last_week}\",\"project_ids\":[187944113,186181587,188328043]}" \
  -u ${TOGGL_API_KEY}:api_token |jq '[.groups | .[]|."sub_groups"|.[]|.seconds]|add')

current_time=$(curl -s  https://api.track.toggl.com/api/v9/me/time_entries/current \
  -H "Content-Type: application/json" \
  -u ${TOGGL_API_KEY}:api_token | jq 'if [.project_id] | inside([187944113,186181587,188328043]) then .start else "empty" end' | tr -d '"')

if [ $current_time = "empty" ]; then
    minutes=0
else
    current_timem=${current_time:0:(-6)}
    minutes=$(( ( $(date '+%s') - $(date -uj -f "%Y-%m-%dT%H:%M:%S" $current_timem '+%s') ) / 60))
fi

total_mins_today=$((minutes + summary_today/60))
total_mins_last_week=$((minutes + summary_last_week/60))

hours_today=$((total_mins_today/60))
mod_mins_today=$((total_mins_today%60))
# pad with leading zero if needed
[[ $mod_mins_today -lt 10 ]] && mod_mins_today="0$mod_mins_today"

echo $total_mins_today > '/Users/danthompson/Code/Scripts/CLI/toggl textbar/data/opt_tooling_time_today.txt'
echo $total_mins_last_week > '/Users/danthompson/Code/Scripts/CLI/toggl textbar/data/opt_tooling_time_last_week.txt'

echo "$hours_today:$mod_mins_today"
