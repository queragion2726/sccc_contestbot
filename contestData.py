from datetime import datetime, timedelta, timezone
from timeStrategy import TimeStrategy

class ContestData:
    def __init__(self, idVal, contestName, startDatetime, URL):
        self.id = idVal
        self.contestName = contestName
        self.startDatetime = startDatetime
        self.URL = URL
        self.ver = 1

    def __repr__(self):
        ret = f'id : {self.id}, name : {self.contestName}, datetime : {self.startDatetime.isoformat()}'
        return ret

class NotiData:
    def __init__(self, contest, timeStrategy):
        self.contest = contest
        self.timeStrategy = timeStrategy
        self.notiTime = contest.startDatetime - timeStrategy.delta
        self.id = contest.id
        self.ver = contest.ver

    def valid(self):
        return self.notiTime > datetime.now(timezone.utc)

    def __gt__(self, o):
        return self.notiTime > o.notiTime
    def __lt__(self, o):
        return self.notiTime < o.notiTime
    def __ge__(self, o):
        return self.notiTime >= o.notiTime
    def __le__(self, o):
        return self.notiTime <= o.notiTime

        