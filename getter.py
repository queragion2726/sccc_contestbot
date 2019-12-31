class Getter:
    def __init__(self, bot, collection):
        self.collection = collection
        self.bot = bot

    # Collect data and put data in self.collection
    def putData(self):
        raise NotImplementedError

    # method for threading
    def start(self):
        raise NotImplementedError

