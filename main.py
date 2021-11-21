import json
from icalendar import Calendar, Event
import requests

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


for component in cal.walk():
    if component.name == "VEVENT":
        print(component.get('summary'))