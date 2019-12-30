class Getter:
    def __init__(self, bot, collection):
        self.collection = collection
        self.bot = bot

    def putData(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

