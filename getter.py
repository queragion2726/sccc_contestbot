class Getter:
    def __init__(self, collection):
        self.collection = collection

    def putData(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

