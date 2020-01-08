from settings import TOKEN
import os
from contestBot import ContestBot

A = ContestBot(TOKEN)
A.run(initNotice=False)