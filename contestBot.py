import threading
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

from timeStrategy import TimeStrategy
from subscriberManager import SubscriberManager
from settings import POST_CHANNEL
from settings import NEW_NOTICE_TXT, NEW_NOTICE_MESSAGE
from settings import MODIFIED_NOTICE_TXT, MODIFIED_NOTICE_MESSAGE
from settings import NOTI_NOTICE_TXT, NOTI_NOTICE_MESSAGE
from settings import CANCELED_NOTICE_TXT, CANCELED_NOTICE_MESSAGE
from settings import SUBSCRIBE_KEYWORD, UNSUBSCRIBE_KEYWORD

import slack

LOGGER = logging.getLogger(__name__)

class ContestBot:
    def __init__(self, token):
        self.eventLoop = asyncio.get_event_loop()
        self.rtmClient = slack.RTMClient(token=token, run_async=True,
                                         loop=self.eventLoop)
        self.webClient = slack.WebClient(token=token, run_async=True,
                                         loop=self.eventLoop)
        self.subscriberManager = SubscriberManager(self)
        self.collectors = []

        slack.RTMClient.run_on(event='message')(self.postSubscriber)
        slack.RTMClient.run_on(event='message')(self.appendSubscriber)
        slack.RTMClient.run_on(event='message')(self.deleteSubscriber)
        slack.RTMClient.run_on(event='message')(self.testPost)

        LOGGER.debug('Bot init')

    def addCollector(self, collectorType):
        self.collectors.append(collectorType(self))

    def start(self, initNotice=True):
        loop = self.eventLoop

        # init update for collectors
        initUpdates = (col.update(repeat=False, noticeOn=initNotice) for col in self.collectors)
        tasks = asyncio.gather(*initUpdates)
        loop.run_until_complete(tasks)

        print('Init update completed')

        # collectors and rtmClient start
        starts = (col.start() for col in self.collectors)
        tasks = asyncio.gather(*starts, self.rtmClient.start())

        import signal
        def stopCallback(signum, frame):
            tasks.cancel()

        signal.signal(signal.SIGINT, stopCallback)
        signal.signal(signal.SIGTERM, stopCallback)

        print('Bot started')

        try:
            loop.run_until_complete(tasks) #run forever
        except asyncio.CancelledError:
            print('Bot Cancelled')
            LOGGER.debug('Bot Cancelled')
        except Exception as e:
            LOGGER.error(e)
            try:
                tasks.cancel()
            except asyncio.CancelledError:
                pass
            raise
        finally:
            loop.stop()

    async def postContest(self, contest, status, notiTimeStrategy=None):
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

        await self.webClient.chat_postMessage(
                channel = POST_CHANNEL,
                text = txt,
                blocks = msg
            )

    async def postText(self, text):
        await self.webClient.chat_postMessage(
            channel = POST_CHANNEL,
            text = text
        )

    async def postSubscriber(self, **payload):
        data = payload['data']
        if 'subtype' in data and data['subtype'] == 'bot_message' \
                            and 'thread_ts' not in data and 'blocks' in data:
            webClient = payload['web_client']
            channel_id = data['channel']
            thread_ts = data['ts']

            subscribe_list = await self.subscriberManager.get()
            text = ' '.join(f'<@{user}>' for user in subscribe_list)
            if text == '':
                return

            await webClient.chat_postMessage(
                    channel = channel_id,
                    text = text,
                    thread_ts = thread_ts
                )

    async def appendSubscriber(self, **payload):
        data = payload['data']
        if 'user' in data and SUBSCRIBE_KEYWORD == data['text']:
            await self.subscriberManager.append(data['user'])

    async def deleteSubscriber(self, **payload):
        data = payload['data']
        if 'user' in data and UNSUBSCRIBE_KEYWORD == data['text']:
            await self.subscriberManager.delete(data['user'])

    async def testPost(self, **payload):
        data = payload['data']
        if 'user' in data and '!Test' in data['text']:
            await payload['web_client'].chat_postMessage(
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


