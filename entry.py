class Entry:
    def __init__(self, title):
        self.title = title


class TimeEntry(Entry):
    def __init__(self, title, dtstart):
        super().__init__(title)
        self.dtstart = dtstart

class DateEntry(Entry):
    def __init__(self, title, dtstart, days):
        super().__init__(title)
        self.dtstart = dtstart
        self.days = days