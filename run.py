from settings import TOKEN
import os
from contestBot import ContestBot
from collectors.codeforcesCollector import CodeforcesCollector
from collectors.baekjoonCollector import BaekjoonCollector

bot = ContestBot(TOKEN)
bot.addCollector(CodeforcesCollector)
bot.addCollector(BaekjoonCollector)
bot.start(initNotice=False)