from datetime import datetime

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

