import datetime
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

class DateEntry(Entry):
    def __init__(self, title, dtstart, days):
        super().__init__(title, dtstart)
        self.days = days



def parse(cal, start_date, end_date):
    result = [];

    events = recurring_ical_events.of(cal).between(start_date, end_date);
    for component in events:
        if component.name == "VEVENT":
            if isinstance(component.get('dtstart').dt, datetime.datetime):
                if component.get('dtend').dt.timestamp() < datetime.datetime.now().timestamp():
                    continue
                entry = TimeEntry(component.get('summary'), component.get('dtstart').dt)
            else:
                if component.get('dtend').dt < datetime.date.today():
                    continue
                entry = DateEntry(component.get('summary'), component.get('dtstart').dt, (component.get('dtend').dt - component.get('dtstart').dt).days)

            result.append(entry)

    
    result.sort()
    return result