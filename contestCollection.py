from contestData import ContestData, NotiData
from datetime import datetime
from settings import *
import threading
import heapq

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
                heapq.heappush(self.notiHeap, NotiData(item, timeStrategy))
                self.heapSize += 1

    def update(self):
        with self.lock:
            while self.heapSize > 0:
                noti = self.notiHeap[0]
                if self.contests[noti.id].ver != noti.ver:
                    heapq.heappop(self.notiHeap)
                    continue
                if noti.timeStrategy == NOTI_STRATEGIES.END:
                    heapq.heappop(self.notiHeap)
                    del self.contests[noti.id]
                    continue

                self.bot.postContest(self.contests[noti.id], status='noti', notiTimeStrategy=noti.timeStrategy)
                heapq.heappop(self.notiHeap)


    def isIDIn(self, idVal):
        with self.lock:
            return idVal in self.contests



