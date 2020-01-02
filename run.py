import settings
import os
from contestBot import ContestBot

token = os.environ('SLACK_TOKEN')

A = ContestBot(token)
A.run()