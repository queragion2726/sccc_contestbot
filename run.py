from settings import TOKEN
import os
from contestBot import ContestBot
from collectors.codeforcesCollector import CodeforcesCollector

bot = ContestBot(TOKEN)
bot.addCollector(CodeforcesCollector)
bot.start(initNotice=False)