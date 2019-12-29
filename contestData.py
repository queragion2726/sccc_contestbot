from datetime import datetime

class ContestData:
    def __init__(self, contestName='None', startDatetime=None, URL=''):
        self.contestName = contestName
        self.URL = URL
        if not startDatetime:
            self.startDatetime = datetime.today()
        else:
            self.startDatetime = startDatetime

    def __lt__(self, o):
        return self.startDatetime < o.startDatetime

    def __gt__(self, o):
        return self.startDatetime > o.startDatetime

    def __le__(self, o):
        return self.startDatetime <= o.startDatetime

    def __ge__(self, o):
        return self.startDatetime >= o.startDatetime

    def __eq__(self, o):
        return self.startDatetime == o.startDatetime

    def __ne__(self, o):
        return self.startDatetime != o.startDatetime

