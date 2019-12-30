from slacker import Slacker
from contestCollection import ContestCollection
from codeforcesGetter import CodeforcesGetter
from settings import *

class ContestBot:
    def __init__(self, token = None, slacker = None):
        if not token and not slacker:
            raise ValueError

        if token is not None:
            self.slack = Slacker(token)
        else:
            self.slack = slacker

        self.contests = ContestCollection()

        # Hard-code area for getters
        self.getterList = []
        self.getterList.append(CodeforcesGetter(self, self.contests))
        #

        self.getContests()
        
    def getContests(self):
        for getter in self.getterList:
            getter.putData()

    def runProcess(self):
        pass

    def postContest(self, contest, status='noti', remain='15분'):
        format_dict = dict()
        format_dict['name'] = contest.contestName
        format_dict['date'] = str(contest.startDatetime)
        format_dict['URL'] = contest.URL
        format_dict['remain'] = remain
        msg = None

        if status == 'new':
            msg = dict(NEW_NOTICE_MESSAGE)
        elif status == 'modified':
            msg = dict(MODIFIED_NOTICE_MESSAGE)
        elif status == 'noti':
            msg = dict(NOTI_NOTICE_MESSAGE)

        msg['pretext'] = msg['pretext'].format(**format_dict)
        msg['title'] = msg['title'].format(**format_dict)
        msg['text'] = msg['text'].format(**format_dict)
        msg['title_link'] = msg['title_link'].format(**format_dict)
        att = [format_dict]
        att.append({'type':'divider'})

        self.slack.chat.post_message(channel=POST_CHANNEL, text=None, attachments=att)
            

