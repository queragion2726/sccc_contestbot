from datetime import datetime, timezone
import json
import threading
import logging
import re

from collectors.collector import Collector
from collectors.collector import ContestData
from settings import LOCAL_TIMEZONE

from bs4 import BeautifulSoup
import aiohttp

LOGGER = logging.getLogger(__name__)

BOJ_PREFIX = 'BOJ'

class BaekjoonData(ContestData):

    def __init__(self, idVal, name, startTime):
        super().__init__(
            idVal,
            name,
            startTime,
            f'https://www.acmicpc.net/contest/view/{str(idVal)}'
        )
        

class BaekjoonCollector(Collector):
    _TARG_URL = 'https://www.acmicpc.net/contest/official/list'
    _UPDATE_INTERVAL = 60*60 # 1 hour
    __RE_REPR = re.compile(r'\d+')

    async def getData(self, noticeOn=True):
        LOGGER.debug(BOJ_PREFIX + " getData()")
        ret = []
        self.attemptCount = 0
        while True:
            self.attemptCount += 1
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self._TARG_URL) as resp:
                        req = await resp.text()
                        soup = BeautifulSoup(req, features='html.parser')
                
                        contestList = soup.find_all('tr', {'class':'info'})
                        for contest in contestList:
                            contents = contest.contents
                            idVal = contents[1].a.attrs['href'].split('/')[-1]
                            name = contents[1].a.text
                            startTime = contents[7].text
                            startTime = datetime(*map(int, self.__RE_REPR.findall(startTime)), tzinfo=LOCAL_TIMEZONE)

                            if startTime < datetime.now(timezone.utc):
                                break

                            data = BaekjoonData(idVal, name, startTime)

                            ret.append(data)
                break
            except aiohttp.ClientError as e:
                LOGGER.error(e)
                await self.errorWait()
                continue
            except Exception as e:
                LOGGER.error(e)
                await self.bot.postText(BOJ_PREFIX+str(e))
                await self.errorWait()
                continue
        return ret



        


