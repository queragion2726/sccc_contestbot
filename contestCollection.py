import threading
import heapq
from contestData import ContestData

# thread-safe priority set-like structure
# it just pair of Heap and dict
class ContestCollection:
    def __init__(self):
        self.lock = threading.Lock()
        self.lastDatetime = dict()
        self.contestHeap = list()
        self.heapSize = 0

    # item should be ContestData 
    def put(self, item):
        if not isinstance(item, ContestData):
            raise TypeError

        with self.lock:
            heapq.heappush(self.contestHeap, item)
            self.lastDatetime[item.id] = item.startDatetime
            self.heapSize += 1

    def get(self):
        with self.lock:
            ret = None

            while self.heapSize > 0:
                firstData = self.contestHeap[0]
                if self.lastDatetime[firstData.id] != firstData.startDatetime:
                    heapq.heappop(self.contestHeap)
                    self.heapSize -= 1
                else:
                    ret = heapq.heappop(self.contestHeap)
                    self.heapSize -= 1
                    del self.lastDatetime[ret.id]
                    break
        return ret
            
    def isModified(self, item):
        if not isinstance(item, ContestData):
            raise TypeError

        with self.lock:
            if item.id not in self.lastDatetime:
                return False

            if self.lastDatetime[item.id] != item.startDatetime:
                return True
            else:
                return False

    def __repr__(self):
        return self.lastDatetime.__repr__() + '\n' + self.contestHeap[0].__repr__()



