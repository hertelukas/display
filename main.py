import datetime
import json
from icalendar import Calendar, Event
from icalendar.cal import Timezone
import requests
from requests.api import get

from entry import DateEntry, Entry, TimeEntry

# read config file
with open('config.dis', 'r') as file:
    config = file.read();

jsonConfig = json.loads(config)


# Download ical file
if jsonConfig['ical']:
    # TODO check status
    cal = Calendar.from_ical(requests.get(jsonConfig['ical']).content)
else:
    print("Failed to get calendar.")

entries = []

for component in cal.walk():
    if component.name == "VEVENT":
        if isinstance(component.get('dtstart').dt, datetime.datetime):
            entry = TimeEntry(component.get('summary'), component.get('dtstart').dt)
        else:
            # TODO parse the duration maybe with dtend or dtstamp
            entry = DateEntry(component.get('summary'), component.get('dtstart').dt, 1)

        entries.append(entry)

