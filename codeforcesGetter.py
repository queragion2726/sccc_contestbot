from getter import Getter
from contestData import ContestData
from datetime import datetime
from settings import LOCAL_TIMEZONE
from time import sleep
import requests
import json
import threading
import logging

LOGGER = logging.getLogger(__name__)

CODEFORCES_PREFIX = 'CF'

class CodeforcesData(ContestData):
    def __init__(self, idVal, name, startTime):
        super().__init__(
            CODEFORCES_PREFIX + str(idVal),
            name,
            datetime.fromtimestamp(startTime, LOCAL_TIMEZONE),
            f'http://codeforces.com/contests/{str(idVal)}'
        )

class CodeforcesGetter(Getter):
    __TARG_URL = 'http://codeforces.com/api/contest.list?gym=false&lang=en'
    __TIME_INTERVAL = 60
    __thicker = threading.Event()

    def putData(self, noticeOn=True):
        req = None
        while True:
            try:
                req = requests.get(self.__TARG_URL)
                if req.status_code >= 500:
                    sleep(10)
                    continue
                break
            except requests.exceptions.ConnectTimeout:
                sleep(10)
                continue
            except requests.exceptions.RequestException as e:
                raise e

        contestList = json.loads(req.text)['result']
        with self.collection:
            for contest in contestList:
                if contest['phase'] != 'BEFORE':
                    break

                data = CodeforcesData(contest['id'],
                                      contest['name'],
                                      contest['startTimeSeconds'])
                self.collection.put(data, noticeOn)

    def start(self):
        try:
            while not self.__thicker.wait(self.__TIME_INTERVAL):
                self.putData()
        except Exception as e:
            self.bot.postError(e)
            LOGGER.error(e)



        


