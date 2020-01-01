import threading

class ScheduleChecker:
    __TIME_INTERVAL = 59 # Prime :)
    __thicker = threading.Event()

    def __init__(self, bot, collection):
        self.bot = bot
        self.collection = collection

    def check(self):
        self.collection.update()

    def start(self):
        while not self.__thicker.wait(self.__TIME_INTERVAL):
            self.check()
