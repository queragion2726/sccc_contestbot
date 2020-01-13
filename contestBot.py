from contestCollection import ContestCollection
from codeforcesGetter import CodeforcesGetter
from scheduleChecker import ScheduleChecker
from subscriberManager import SubscriberManager
from timeStrategy import TimeStrategy
from settings import GETTERS, POST_CHANNEL
from settings import NEW_NOTICE_TXT, NEW_NOTICE_MESSAGE
from settings import MODIFIED_NOTICE_TXT, MODIFIED_NOTICE_MESSAGE
from settings import NOTI_NOTICE_TXT, NOTI_NOTICE_MESSAGE
from settings import CANCELED_NOTICE_TXT, CANCELED_NOTICE_MESSAGE
from settings import SUBSCRIBE_KEYWORD, UNSUBSCRIBE_KEYWORD
import slack
import threading
import logging

LOGGER = logging.getLogger(__name__)

class ContestBot:
    def __init__(self, token):
        self.webClient = slack.WebClient(token=token)
        self.rtmClient = slack.RTMClient(token=token)

        self.contests = ContestCollection(self)
        self.getterList = []
        self.scheduleChecker = ScheduleChecker(self, self.contests)
        self.subscriberManager = SubscriberManager(self)

        for Getter in GETTERS:
            Getter = Getter.value # getter type
            self.getterList.append(Getter(self, self.contests)) # construct getter instance

        slack.RTMClient.run_on(event='message')(self.postSubscriber)
        slack.RTMClient.run_on(event='message')(self.appendSubscriber)
        slack.RTMClient.run_on(event='message')(self.deleteSubscriber)
        slack.RTMClient.run_on(event='message')(self.testPost)

        LOGGER.info('Bot init')
    
    def run(self, initNotice=True):
        self.getContests(initNotice)
        self.runThreads()
        self.rtmClient.start()
        
    def getContests(self, noticeOn=True):
        for getter in self.getterList:
            getter.putData(noticeOn)

    def runThreads(self):
        threads = []
        for getter in self.getterList:
            threads.append(threading.Thread(target=getter.start))
        threads.append(threading.Thread(target=self.scheduleChecker.start))
        for thread in threads:
            thread.start()

    def postContest(self, contest, status, notiTimeStrategy=None):
        if status == 'noti' and not isinstance(notiTimeStrategy, TimeStrategy):
            raise TypeError
        format_dict = {
            'name': contest.contestName,
            'datetime': str(contest.startDatetime),
            'URL': contest.URL,
            'remain': 'None'
        }

        if notiTimeStrategy:
            format_dict['remain'] = notiTimeStrategy.displayText

        txt = None
        msg = None

        if status == 'new':
            txt = NEW_NOTICE_TXT % format_dict
            msg = NEW_NOTICE_MESSAGE % format_dict
        elif status == 'modified':
            txt = MODIFIED_NOTICE_TXT % format_dict
            msg = MODIFIED_NOTICE_MESSAGE % format_dict
        elif status == 'noti':
            txt = NOTI_NOTICE_TXT % format_dict
            msg = NOTI_NOTICE_MESSAGE % format_dict
        elif status == 'canceled':
            txt = CANCELED_NOTICE_TXT % format_dict
            msg = CANCELED_NOTICE_MESSAGE % format_dict

        self.webClient.chat_postMessage(
            channel = POST_CHANNEL,
            text = txt,
            blocks = msg
        )

    def postError(self, e):
        self.webClient.chat_postMessage(
            channel = POST_CHANNEL,
            text = str(e)
        )

    def postText(self, txt):
        self.webClient.chat_postMessage(
            channel = POST_CHANNEL,
            text = txt
        )

    def postSubscriber(self, **payload):
        data = payload['data']
        if 'subtype' in data and data['subtype'] == 'bot_message' \
                            and 'thread_ts' not in data and 'blocks' in data:
            webClient = payload['web_client']
            channel_id = data['channel']
            thread_ts = data['ts']
            text = ' '.join((f'<@{user}>' for user in self.subscriberManager.get()))
            if text == '':
                return
            webClient.chat_postMessage(
                channel = channel_id,
                text = text,
                thread_ts = thread_ts
            )

    def appendSubscriber(self, **payload):
        data = payload['data']
        if 'user' in data and SUBSCRIBE_KEYWORD == data['text']:
            self.subscriberManager.append(data['user'])

    def deleteSubscriber(self, **payload):
        data = payload['data']
        if 'user' in data and UNSUBSCRIBE_KEYWORD == data['text']:
            self.subscriberManager.delete(data['user'])


    def testPost(self, **payload):
        data = payload['data']
        if 'user' in data and '!Test' in data['text']:
            payload['web_client'].chat_postMessage(
                channel = POST_CHANNEL,
                text = 'test!',
                blocks=[{
			        "type": "section",
			        "text": {
			        	"type": "mrkdwn",
			        	"text": "Test"
			        }
		        }]
            ) 


