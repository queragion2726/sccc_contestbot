from contestData import ContestData
from datetime import datetime
import threading
import heapq

class ContestCollection:
    def __init__(self):
        self.lock = threading.Lock()
        self.contests = dict()
        self.notiHeap = list()
        self.heapSize = 0

    # item should be ContestData 
    def put(self, item):
        if not isinstance(item, ContestData):
            raise TypeError

        with self.lock:
            self.contests[item.id] = item
            # TODO : notification interval set
            heapq.heappush(self.notiHeap, (item.startDatetime, item.id, item.ver))
            self.heapSize += 1

    def isIDIn(self, idVal):
        with self.lock:
            return idVal in self.contests



