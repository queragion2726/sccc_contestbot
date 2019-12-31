from contestCollection import ContestCollection
from codeforcesGetter import CodeforcesGetter
from settings import *
import slack
import threading

class ContestBot:
    def __init__(self, token = None, slackClient = None):
        if not token and not slackClient:
            raise ValueError

        if token is not None:
            self.slack = slack.WebClient(token=token)
        else:
            self.slack = slackClient

        self.contests = ContestCollection()

        # Hard-code area for getters
        self.getterList = []
        self.getterList.append(CodeforcesGetter(self, self.contests))
        #

        self.getContests()
        self.runThreads()
        
    def getContests(self):
        for getter in self.getterList:
            getter.putData()

    def runThreads(self):
        threads = []
        for getter in self.getterList:
            threads.append(threading.Thread(target=getter.start))
        for thread in threads:
            thread.start()

    def postContest(self, contest, status='noti', remain='15분'):
        format_dict = {
            'name': contest.contestName,
            'datetime': str(contest.startDatetime),
            'URL': contest.URL,
            'remain': remain
        }

        txt = None
        msg = None

        if status == 'new':
            txt = NEW_NOTICE_TXT.format(**format_dict)
            msg = NEW_NOTICE_MESSAGE.format(**format_dict)
        elif status == 'modified':
            txt = MODIFIED_NOTICE_TXT.format(**format_dict)
            msg = MODIFIED_NOTICE_MESSAGE.format(**format_dict)
        elif status == 'noti':
            txt = NOTI_NOTICE_TXT.format(**format_dict)
            msg = NOTI_NOTICE_MESSAGE.format(**format_dict)

        self.slack.chat_postMessage(
            channel = POST_CHANNEL,
            text = txt,
            blocks = msg
        )
            

