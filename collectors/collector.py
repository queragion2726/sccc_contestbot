import threading
import asyncio
import enum
import heapq
import logging
from datetime import datetime, timedelta, timezone

from settings import NOTI_STRATEGIES
from timeStrategy import TimeStrategy

from slack import WebClient

LOGGER = logging.getLogger(__name__)

class ContestData:
    def __init__(self, idVal, contestName, startDatetime, URL):
        self.id = idVal
        self.contestName = contestName
        self.startDatetime = startDatetime
        self.URL = URL

    def __repr__(self):
        ret = f'id : {self.id}, name : {self.contestName}, datetime : {self.startDatetime.isoformat()}'
        return ret

    def __eq__(self, o):
        return self.id == o.id and                       \
               self.startDatetime == o.startDatetime and \
               self.URL == o.URL

class NotiData:
    def __init__(self, contest, group, timeStrategy):
        self.contest = contest
        self.group = group 
        self.timeStrategy = timeStrategy
        self.notiTime = contest.startDatetime - timeStrategy.delta
        self.id = contest.id

    def validNotiTime(self):
        return self.notiTime > datetime.now(timezone.utc)

    def valid(self):
        if self.id not in self.group:
            return False

        return self.contest is self.group[self.id] 

    def __gt__(self, o):
        return self.notiTime > o.notiTime
    def __lt__(self, o):
        return self.notiTime < o.notiTime
    def __ge__(self, o):
        return self.notiTime >= o.notiTime
    def __le__(self, o):
        return self.notiTime <= o.notiTime

class Collector:
    _CHECK_INTERVAL = 59
    _UPDATE_INTERVAL = 61 # coprime with 59 :)
    _MAX_ERROR_WAIT_TIME = 60*20

    def __init__(self, bot):
        self.lock = asyncio.Lock()
        self.bot = bot
        self.contests = dict()
        self.notiHeap = list()
        self.attemptCount = 0

    def openPutManager(self):
        putManager = self.PutManager(
            self.contests, 
            self.notiHeap, 
            self.lock,
            self.bot)
        return putManager
    
    class PutManager:
        def __init__(self, contests, notiHeap, lock, bot):
            self.putCheck = dict()
            self.contests = contests
            self.notiHeap = notiHeap
            self.lock = lock
            self.bot = bot

        async def __aenter__(self):
            await self.lock.acquire()
            self.putCheck.clear()
            for idVal in self.contests:
                self.putCheck[idVal] = False
            return self

        async def __aexit__(self, *args):
            for idVal in self.putCheck:
                if not self.putCheck[idVal]:
                    await self.bot.postContest(
                        self.contests[idVal], 
                        status='canceled'
                    )
                    del self.contests[idVal]
            self.lock.release()
            return

        async def put(self, item, noticeOn = True):
            # item should be ContestData 
            if not isinstance(item, ContestData):
                raise TypeError

            self.putCheck[item.id] = True

            if item.id in self.contests:
                if item == self.contests[item.id]:
                    return
                self.contests[item.id] = item
                if noticeOn:
                    await self.bot.postContest(item, status='modified')
            else:
                self.contests[item.id] = item
                if noticeOn:
                    await self.bot.postContest(item, status='new')

            for timeStrategy in NOTI_STRATEGIES:
                timeStrategy = timeStrategy.value
                noti = NotiData(item, self.contests, timeStrategy)

                if noti.validNotiTime():
                    heapq.heappush(self.notiHeap, noti)
                    logging.debug('noti put ' + str(noti.notiTime) +
                                   ' ' + noti.contest.contestName)

    async def getData(self):
        raise NotImplementedError

    async def update(self, repeat=True, noticeOn=True):
        async with self.openPutManager() as putter:
            for data in await self.getData():
                await putter.put(data, noticeOn)
        
        if not repeat:
            return

        while True:
            async with self.openPutManager() as putter:
                for data in await self.getData():
                    await putter.put(data, noticeOn)
            await asyncio.sleep(self._UPDATE_INTERVAL)

    async def popCheck(self):
        while True:
            LOGGER.debug("pop check")
            async with self.lock:
                while len(self.notiHeap) > 0:
                    noti = self.notiHeap[0]
                    LOGGER.debug(
                        'noti cur : ' + str(noti.notiTime) 
                        + ' ' + noti.contest.contestName)

                    if not noti.valid():
                        heapq.heappop(self.notiHeap)
                        continue
                    
                    if noti.validNotiTime():
                        break

                    if noti.timeStrategy == NOTI_STRATEGIES.END.value:
                        heapq.heappop(self.notiHeap)
                        del noti.group[noti.id]
                        continue

                    await self.bot.postContest(
                        noti.group[noti.id], 
                        status='noti', 
                        notiTimeStrategy=noti.timeStrategy
                    )
                    heapq.heappop(self.notiHeap)
            LOGGER.debug("check end")
            await asyncio.sleep(self._CHECK_INTERVAL)

    async def start(self):
        try:
            await asyncio.gather(
                    self.update(),
                    self.popCheck()
                )
        except asyncio.CancelledError:
            return

    async def errorWait(self):
        waitTime = min(2**self.attemptCount, self._MAX_ERROR_WAIT_TIME)
        await asyncio.sleep(waitTime)



