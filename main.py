import json
from icalendar import Calendar
import requests
import datetime

from entry import DateEntry, Entry, TimeEntry, parse
from weather import get_forecast

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

today = datetime.date.today();

# Parse the entries for the next 7 days
entries = parse(cal, today, today + datetime.timedelta(days=7))

# Get weather data
forecast = get_forecast(jsonConfig['lat'], jsonConfig['lon'], 3, jsonConfig['api'])

for item in forecast:
    print(item.max)
    print(item.min)