from datetime import datetime

class ContestData:
    def __init__(self, contestName='None', startDatetime=datetime.today(), endDatetime=datetime.today(), URL=''):
        self.contestName = contestName
        self.startDate = startDate
        self.endDate = endDatetime
        self.URL = URL
