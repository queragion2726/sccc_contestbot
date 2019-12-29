from datetime import datetime

class ContestData:
    def __init__(self, contestName='None', startDatetime=None, URL=''):
        self.contestName = contestName
        self.URL = URL
        if not startDatetime:
            self.startDatetime = datetime.today()
        else:
            self.startDatetime = startDatetime

        



