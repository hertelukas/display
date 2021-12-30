import datetime
import re
import recurring_ical_events

class Entry:
    def __init__(self, title, dtstart):
        self.title = title
        self.dtstart = dtstart

    def __lt__(self, other):
        if isinstance(self.dtstart, datetime.datetime) and not isinstance(other.dtstart, datetime.datetime):
            return self.dtstart.date() < other.dtstart

        if isinstance(other.dtstart, datetime.datetime) and not isinstance(self.dtstart, datetime.datetime):
            return self.dtstart < other.dtstart.date()

        return self.dtstart < other.dtstart


class TimeEntry(Entry):
    def __init__(self, title, dtstart):
        super().__init__(title, dtstart)
    
    def to_string(self):
        return self.dtstart.astimezone().strftime("%H:%M ") + self.title
        

class DateEntry(Entry):
    def __init__(self, title, dtstart, days):
        super().__init__(title, dtstart)
        self.days = days

    def to_string(self):
        return self.title


class Day:
    def __init__(self, date):
        self.date = date
        self.items = []

    def add(self, summary):
        self.items.append(summary)


def parse(cal, start_date, end_date):
    result = [];

    events = recurring_ical_events.of(cal).between(start_date, end_date);
    for component in events:
        if component.name == "VEVENT":
            if isinstance(component.get('dtstart').dt, datetime.datetime):
                entry = TimeEntry(component.get('summary'), component.get('dtstart').dt)
            else:
                if component.get('dtend').dt == start_date:
                    continue
                entry = DateEntry(component.get('summary'), component.get('dtstart').dt, (component.get('dtend').dt - component.get('dtstart').dt).days)

            result.append(entry)

    
    result.sort()
    return result

def get_next_days(cal, days):
    result = [];

    for i in range(days):
        day = datetime.date.today() + datetime.timedelta(days=i)
        current = Day(day)
        events = parse(cal, day, day + datetime.timedelta(days=1))

        for event in events:
            current.add(event.to_string())
        
        result.append(current)

    return result