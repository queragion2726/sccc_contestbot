from datetime import timedelta


class TimeStrategy:
    def __init__(self, displayText, days=0, hours=0, minutes=0, seconds=0):
        self.delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        self.displayText = displayText
