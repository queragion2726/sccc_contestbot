from datetime import datetime

class ContestData:
    def __init__(self, idVal, contestName='None', startDatetime=None, URL=''):
        self.id = idVal
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


    def __repr__(self):
        ret = f'id : {self.id}, name : {self.contestName}, datetime : {self.startDatetime.isoformat()}'
        return ret

