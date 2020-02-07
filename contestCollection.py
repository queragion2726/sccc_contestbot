from contestData import ContestData, NotiData
from datetime import datetime
from settings import NOTI_STRATEGIES, GETTERS
import threading
import heapq
import logging

LOGGER = logging.getLogger(__name__)

class ContestCollection:
    def __init__(self, bot):
        self.lock = threading.Lock()
        self.contestGroups = dict()
        self.notiHeap = list()

        for getter in GETTERS:
            getter = getter.value
            self.contestGroups[getter.getPrefix()] = dict()


    def open(self, prefixKey, webClient):
        ret = None
        with self.lock:
            ret = self.PutHandler(self, prefixKey, webClient)
        return ret

    class PutHandler:
        def __init__(self, collection, prefixKey, webClient):
            self.lock = collection.lock
            self.group = collection.contestGroups[prefixKey]
            self.notiHeap = collection.notiHeap
            self.webClient = webClient
            self.putCheck = dict()

        def __enter__(self):
            self.lock.acquire()
            self.putCheck.clear()
            for idVal in self.group:
                self.putCheck[idVal] = False
            return self

        def __exit__(self, type, value, traceback):
            for idVal in self.putCheck:
                if not self.putCheck[idVal]:
                    self.bot.postContest(self.group[idVal], 'canceled')
                    del self.group[idVal]
            self.lock.release()
            return

        def put(self, item, noticeOn):
            # item should be ContestData 
            if not isinstance(item, ContestData):
                raise TypeError

            self.putCheck[item.id] = True

            if item.id in self.group:
                if item.startDatetime == self.group[item.id].startDatetime:
                    return
                item.ver = self.group[item.id].ver + 1
                self.group[item.id] = item
                if noticeOn:
                    self.bot.postContest(item, status='modified', self.webClient)
            else:
                self.group[item.id] = item
                if noticeOn:
                    self.bot.postContest(item, status='new', self.webClient)

            for timeStrategy in NOTI_STRATEGIES:
                timeStrategy = timeStrategy.value
                noti = NotiData(item, self.group, timeStrategy)

                if noti.valid():
                    heapq.heappush(self.notiHeap, noti)
                    logging.debug('noti put ' + str(noti.notiTime) +
                                   ' ' + noti.contest.contestName)

    def update(self):
        logging.debug('notiheap update, notiheap size : ' + str(len(self.notiHeap)))
        with self.lock:
            while len(self.notiHeap) > 0:
                noti = self.notiHeap[0]
                logging.debug('noti cur : ' + str(noti.notiTime) + ' ' + noti.contest.contestName)

                if noti.id not in noti.group:
                    heapq.heappop(self.notiHeap)
                    continue
                if noti.group[noti.id].ver != noti.ver:
                    heapq.heappop(self.notiHeap)
                    continue

                if noti.valid():
                    break

                if noti.timeStrategy == NOTI_STRATEGIES.END.value:
                    heapq.heappop(self.notiHeap)
                    del noti.group[noti.id]
                    continue

                self.bot.postContest(noti.group[noti.id], status='noti', notiTimeStrategy=noti.timeStrategy)
                heapq.heappop(self.notiHeap)
        logging.debug('update END')
