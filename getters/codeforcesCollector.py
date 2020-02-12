import json
import threading
import logging

from getters.collector import Collector
from getters.collector import ContestData
from datetime import datetime
from settings import LOCAL_TIMEZONE, POST_CHANNEL
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
    #_TARG_URL = 'http://codeforces.com/api/contest.list?gym=false&lang=en'
    _TARG_URL = 'http://127.0.0.1/'

    async def getData(self, noticeOn=True):
        LOGGER.debug(CODEFORCES_PREFIX + " getData()")
        ret = []
        self.attemptCount = 0
        while True:
            self.attemptCount += 1
            try:
                async with aiohttp.ClientSession(raise_for_status=True) as session:
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
                break
            except aiohttp.ClientError as e:
                LOGGER.error(e)
                await self.errorWait()
                continue
            except Exception as e:
                LOGGER.error(e)
                await self.webClient.chat_postMessage(
                    channel = POST_CHANNEL,
                    text=str(e)
                )
                await self.errorWait()
                continue

        return ret



        


