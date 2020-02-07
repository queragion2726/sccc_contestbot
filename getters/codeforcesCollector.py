import json
import threading
import logging

from getters.collector import Collector
from getters.collector import ContestData
from datetime import datetime
from settings import LOCAL_TIMEZONE
from time import sleep

import aiohttp


LOGGER = logging.getLogger(__name__)

CODEFORCES_PREFIX = 'CF'

class CodeforcesData(ContestData):
    def __init__(self, idVal, name, startTime):
        super().__init__(
            idVal,
            name,
            datetime.fromtimestamp(startTime, LOCAL_TIMEZONE),
            f'http://codeforces.com/contests/{str(idVal)}'
        )

class CodeforcesCollector(Collector):
    _TARG_URL = 'http://codeforces.com/api/contest.list?gym=false&lang=en'
    #_TARG_URL = 'http://127.0.0.1/'

    async def getData(self, noticeOn=True):
        ret = []
        async with aiohttp.ClientSession() as session:
            async with session.get(self._TARG_URL) as resp:
                txt = await resp.text()
                contestList = json.loads(txt)['result']
                for contest in contestList:
                    if contest['phase'] != 'BEFORE':
                        break
                data = CodeforcesData(contest['id'],
                                      contest['name'],
                                      contest['startTimeSeconds'])
                ret.append(data)
        return ret



        


