from getter import Getter
from contestData import ContestData
from datetime import datetime
from settings import LOCAL_TIMEZONE
import requests
import json
import threading

CODEFORCES_PREFIX = 'CF'

class CodeforcesData(ContestData):
    def __init__(self, idVal, name, startTime):
        self.id = CODEFORCES_PREFIX + str(idVal)
        self.contestName = name
        self.startDatetime = datetime.fromtimestamp(startTime, LOCAL_TIMEZONE)
        self.URL = f'http://codeforces.com/contests/{str(idVal)}'

class CodeforcesGetter(Getter):
    __TARG_URL = 'http://codeforces.com/api/contest.list?gym=false&lang=en'
    __TIME_INTERVAL = 60
    __thicker = threading.Event()

    def putData(self):
        req = requests.get(self.__TARG_URL)
        contestList = json.loads(req.text)['result']
        for contest in contestList:
            if contest['phase'] != 'BEFORE':
                break

            data = CodeforcesData(contest['id'],
                                  contest['name'],
                                  contest['startTimeSeconds'])

            if self.collection.isIDIn(data.id):
                if self.collection.isModified(data):
                    self.bot.postContest(data, status='modified')
                    self.collection.put(data)
            else:
                self.bot.postContest(data, status='new')
                self.collection.put(data)

    def start(self):
        while not self.__thicker.wait(self.__TIME_INTERVAL):
            self.putData()



        


