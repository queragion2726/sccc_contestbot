from slacker import Slacker
from queue import PriorityQueue

class ContestBot:
    def __init__(self, token = None, slacker = None):
        if not token and not slacker:
            raise ValueError

        if token is not None:
            self.slack = Slacker(token)
        else:
            self.slack = slacker

        self.contestQueue = PriorityQueue()

        
        

    def getContests():
        pass

    def runProcess():
        pass

