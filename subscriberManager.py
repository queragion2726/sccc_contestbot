from settings import NO_SUCH_USER, ALREADY_EXISTS
from settings import APPEND_SUCCESS, DELETE_SUCCESS
import threading
import logging
import re

LOGGER = logging.getLogger(__name__)

class SubscriberManager:
    __FILE_NAME = 'subscriber.list'
    __RE_REPR = re.compile(r'\S+')

    def __init__(self, bot):
        self.lock = threading.Lock()
        self.bot = bot
        self.lists = []
        with open(self.__FILE_NAME, 'r') as file:
            for item in self.__RE_REPR.findall(file.read()):
                self.lists.append(item)

    def get(self):
        ret = None
        with self.lock:
            ret = iter(self.lists)
        return ret
    
    def delete(self, user):
        with self.lock:
            try:
                self.lists.remove(user)
            except ValueError:
                self.bot.postText(NO_SUCH_USER)
                LOGGER.debug(user + 'delete failed')
                return
            
            with open(self.__FILE_NAME, 'w') as file:
                file.writelines(iter(self.lists))
        self.bot.postText(DELETE_SUCCESS)
        LOGGER.debug(user + 'deleted')
    
    def append(self, user):
        with self.lock:
            if user in self.lists:
                self.bot.postText(ALREADY_EXISTS)
                LOGGER.debug(user + 'already exists')
                return
            with open(self.__FILE_NAME, 'a') as file:
                file.write(user + '\n')
            self.lists.append(user)
        self.bot.postText(APPEND_SUCCESS)
        LOGGER.debug(user + 'appended')



