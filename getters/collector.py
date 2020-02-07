import threading
import asyncio
import enum
import heapq
import logging
from datetime import datetime, timedelta, timezone

from contestBot import ContestBot
from settings import NOTI_STRATEGIES
from timeStrategy import TimeStrategy

from slack import WebClient

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

class Collector:
    _CHECK_INTERVAL = 59
    _UPDATE_INTERVAL = 61 # coprime with 59 :)

    def __init__(self, token):
        self.lock = asyncio.Lock()
        self.webClient = WebClient(token=token, run_async=True)
        self.contests = dict()
        self.notiHeap = list()
        self.eventLoop = None

    def openPutManager(self):
        putManager = self.PutManager(
            self.contests, 
            self.notiHeap, 
            self.lock,
            self.webClient)
        return putManager
    
    class PutManager:
        def __init__(self, contests, notiHeap, lock, webClient):
            self.putCheck = dict()
            self.contests = contests
            self.notiHeap = notiHeap
            self.lock = lock
            self.webClient = webClient

        async def __aenter__(self):
            await self.lock.acquire()
            self.putCheck.clear()
            for id in self.contests:
                self.putCheck[id] = False
            return self

        async def __aexit__(self, *args):
            for id in self.putCheck:
                if not self.putCheck[id]:
                    await ContestBot.postContest(
                        self.contests[id], 
                        status='canceled', 
                        webClient=self.webClient
                    )
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
                    await ContestBot.postContest(item, status='modified', webClient=self.webClient)
            else:
                self.contests[item.id] = item
                if noticeOn:
                    await ContestBot.postContest(item, status='new', webClient=self.webClient)

            for timeStrategy in NOTI_STRATEGIES:
                timeStrategy = timeStrategy.value
                noti = NotiData(item, self.contests, timeStrategy)

                if noti.valid():
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
            try:
                async with self.openPutManager() as putter:
                    for data in await self.getData():
                        await putter.put(data, noticeOn)
                await asyncio.sleep(self._UPDATE_INTERVAL)
            except asyncio.CancelledError:
                break

    async def popCheck(self):
        while True:
            try:
                async with self.lock:
                    pass
                await asyncio.sleep(self._CHECK_INTERVAL)
            except asyncio.CancelledError:
                break

    async def start(self):
        await asyncio.gather(
                    self.update(),
                    self.popCheck()
                )


