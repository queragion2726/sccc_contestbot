from contestData import ContestData, NotiData
from datetime import datetime
from settings import NOTI_STRATEGIES
import threading
import heapq
import logging

LOGGER = logging.getLogger(__name__)

class ContestCollection:
    def __init__(self, bot):
        self.lock = threading.Lock()
        self.contests = dict()
        self.notiHeap = list()
        self.bot = bot
        self.heapSize = 0

    # item should be ContestData 
    def put(self, item):
        if not isinstance(item, ContestData):
            raise TypeError

        with self.lock:
            if item.id in self.contests:
                if item.startDatetime == self.contests[item.id].startDatetime:
                    return
                item.ver = self.contests[item.id].ver + 1
                self.contests[item.id] = item
                self.bot.postContest(item, status='modified')
            else:
                self.contests[item.id] = item
                self.bot.postContest(item, status='new')

            for timeStrategy in NOTI_STRATEGIES:
                timeStrategy = timeStrategy.value
                noti = NotiData(item, timeStrategy)

                if noti.valid():
                    heapq.heappush(self.notiHeap, noti)
                    self.heapSize += 1
                    logging.debug('noti put ' + str(noti.notiTime) + ' ' + noti.contest.contestName)

    def update(self):
        with self.lock:
            logging.debug('notiheap update : ' +  str(datetime.now()))
            while self.heapSize > 0:
                noti = self.notiHeap[0]
                if self.contests[noti.id].ver != noti.ver:
                    heapq.heappop(self.notiHeap)
                    self.heapSize -= 1
                    continue

                logging.debug('noti cur : ' + str(noti.notiTime) + ' ' + noti.contest.contestName)

                if noti.valid():
                    logging.debug('update END')
                    return

                if noti.timeStrategy == NOTI_STRATEGIES.END.value:
                    heapq.heappop(self.notiHeap)
                    del self.contests[noti.id]
                    self.heapSize -= 1
                    continue

                self.bot.postContest(self.contests[noti.id], status='noti', notiTimeStrategy=noti.timeStrategy)
                heapq.heappop(self.notiHeap)
                self.heapSize -= 1


    def isIDIn(self, idVal):
        with self.lock:
            return idVal in self.contests



