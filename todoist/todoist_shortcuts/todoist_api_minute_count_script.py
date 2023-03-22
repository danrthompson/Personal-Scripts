import os

import todoist
import re
from datetime import datetime

api = todoist.TodoistAPI(os.environ.get('TODOIST_API_KEY'))

qcs_id = [project['id'] for  project in  api.state['projects'] if project['name'] == 'Quick clean slate']
if len(qcs_id) != 1:
    # exit
    pass
qcs_id = qcs_id[0]

today_date = date.today().strftime('%Y-%m-%d')
today_re = today_date + '(:?T\d+:)?'
today_re = re.compile(today_re)

tasks = api.items.all(filt=lambda item: item['project_id'] == qcs_id)
task_names = [task['content'] for task in tasks if task['due'] and today_re.match(task['due']['date'])]

matches = [re.search('//(\d+)m', task_name) for task_name in task_names]
durations = [match.groups()[0] for match in matches if match and len(match.groups()) == 1]
durations = [int(duration) for duration in durations if duration.isdigit()]

total_mins = sum(durations)
total_hours = total_mins / 60