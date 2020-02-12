import asyncio
import logging
import re

from settings import NO_SUCH_USER, ALREADY_EXISTS
from settings import APPEND_SUCCESS, DELETE_SUCCESS

LOGGER = logging.getLogger(__name__)

class SubscriberManager:
    __FILE_NAME = 'subscriber.list'
    __RE_REPR = re.compile(r'\S+')

    def __init__(self, bot):
        self.lock = asyncio.Lock()
        self.bot = bot
        self.lists = []
        with open(self.__FILE_NAME, 'r') as file:
            for item in self.__RE_REPR.findall(file.read()):
                self.lists.append(item)

    async def get(self):
        async with self.lock:
            ret = iter(self.lists)
        return ret
    
    async def delete(self, user):
        async with self.lock:
            try:
                self.lists.remove(user)
            except ValueError:
                await self.bot.postText(NO_SUCH_USER)
                LOGGER.debug(user + 'delete failed')
                return
            
            with open(self.__FILE_NAME, 'w') as file:
                file.writelines(iter(self.lists))
        await self.bot.postText(DELETE_SUCCESS)
        LOGGER.debug(user + 'deleted')
    
    async def append(self, user):
        async with self.lock:
            if user in self.lists:
                await self.bot.postText(ALREADY_EXISTS)
                LOGGER.debug(user + 'already exists')
                return
            with open(self.__FILE_NAME, 'a') as file:
                file.write(user + '\n')
            self.lists.append(user)
        await self.bot.postText(APPEND_SUCCESS)
        LOGGER.debug(user + 'appended')

