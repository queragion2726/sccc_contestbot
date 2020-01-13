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
        self.putChk = dict()
        self.notiHeap = list()
        self.bot = bot

    def __enter__(self):
        self.lock.acquire()
        self.putChk.clear()
        for idVal in self.contests:
            self.putChk[idVal] = False
        return self

    def __exit__(self, type, value, traceback):
        for idVal in self.putChk:
            if not self.putChk[idVal]:
                self.bot.postContest(self.contests[idVal], 'canceled')
                del self.contests[idVal]
        self.lock.release()

    def put(self, item, noticeOn):
        # item should be ContestData 
        # You should put items with following codes;
        '''
        with collection:
            for data in contest
                collection.put(data)
        '''
        if not isinstance(item, ContestData):
            raise TypeError

        self.putChk[item.id] = True

        if item.id in self.contests:
            if item.startDatetime == self.contests[item.id].startDatetime:
                return
            item.ver = self.contests[item.id].ver + 1
            self.contests[item.id] = item
            if noticeOn:
                self.bot.postContest(item, status='modified')
        else:
            self.contests[item.id] = item
            if noticeOn:
                self.bot.postContest(item, status='new')

        for timeStrategy in NOTI_STRATEGIES:
            timeStrategy = timeStrategy.value
            noti = NotiData(item, timeStrategy)

            if noti.valid():
                heapq.heappush(self.notiHeap, noti)
                logging.debug('noti put ' + str(noti.notiTime) +
                               ' ' + noti.contest.contestName)

    def update(self):
        with self.lock:
            logging.debug('notiheap update : ' +  str(datetime.now()))
            while len(self.notiHeap) > 0:
                noti = self.notiHeap[0]
                if noti.id not in self.contests:
                    heapq.heappop(self.notiHeap)
                    continue
                if self.contests[noti.id].ver != noti.ver:
                    heapq.heappop(self.notiHeap)
                    continue

                logging.debug('noti cur : ' + str(noti.notiTime) + ' ' + noti.contest.contestName)

                if noti.valid():
                    logging.debug('update END')
                    return

                if noti.timeStrategy == NOTI_STRATEGIES.END.value:
                    heapq.heappop(self.notiHeap)
                    del self.contests[noti.id]
                    continue

                self.bot.postContest(self.contests[noti.id], status='noti', notiTimeStrategy=noti.timeStrategy)
                heapq.heappop(self.notiHeap)


    def isIDIn(self, idVal):
        with self.lock:
            return idVal in self.contests



