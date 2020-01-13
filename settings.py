from datetime import datetime, timedelta
from timeStrategy import TimeStrategy
from enum import Enum
import os
import logging

logging.basicConfig(filename='log.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo
POST_CHANNEL = '#dev-playground'
#POST_CHANNEL = '#대회_알림_공지방'
TOKEN = os.environ.get('SLACK_API_TOKEN')

# Getters
# You can append additional getter implementations to GETTERS class
from codeforcesGetter import CodeforcesGetter
class GETTERS(Enum):
    CODEFORCES = CodeforcesGetter

# Notification strategies
# END var is necessary. Don't remove it.
class NOTI_STRATEGIES(Enum):
    END = TimeStrategy("for remove", seconds=0)
    BEFORE_10MINUTES = TimeStrategy(displayText="10분", minutes=10)
    BEFORE_1HOURS = TimeStrategy(displayText="1시간", hours=1)
    BEFORE_3HOURS = TimeStrategy(displayText="3시간", hours=3)
    BEFORE_1DAYS = TimeStrategy(displayText="하루", days=1)

# NOTICE_TXT will be displayed on app notification, not message.
# NOTICE_MESSAGE will be displayed like normal message you know.
# NOTE: NOTICE_MESSAGE should be blocks format. Please check on slack api pages.
# https://api.slack.com/block-kit
# You can use some formatting to represent the contest information.
# %(name)s : contest name
# %(datetime)s : start datetime of contest
# %(remain)s : remaining time; value of TimeStrategy.dispalayText
# %(URL)s : URL of contest page

NEW_NOTICE_TXT = '%(name)s 등록되었습니다!'
NEW_NOTICE_MESSAGE = """
[
    {
		'type': 'section',
		'text': {
			'type': 'mrkdwn',
			'text': '*<%(URL)s|%(name)s>*'
		}
	},
	{
		'type': 'context',
		'elements': [
            {
                'type': 'mrkdwn',
                'text': '*새로운 대회가 등록되었습니다!! *:blobaww:\n'
            }
        ]
    },
    {
        'type': 'context',
        'elements': [
			{
				'type': 'mrkdwn',
				'text': '시작시각 : %(datetime)s'
			}
		]
	},
	{
		'type': 'divider'
	}
]
"""

MODIFIED_NOTICE_TXT = '%(name)s 일정이 변경되었습니다.'
MODIFIED_NOTICE_MESSAGE = """
[
    {
		'type': 'section',
		'text': {
			'type': 'mrkdwn',
			'text': '*<%(URL)s|%(name)s>*'
		}
	},
	{
		'type': 'context',
		'elements': [
            {
                'type': 'mrkdwn',
                'text': '*대회 일정이 변경되었습니다... *:blobsob:\n'
            }
        ]
    },
    {
        'type': 'context',
        'elements': [
			{
				'type': 'mrkdwn',
				'text': '시작시각 : %(datetime)s'
			}
		]
	},
	{
		'type': 'divider'
    }
]
"""

NOTI_NOTICE_TXT = '%(name)s %(remain)s 전!'
NOTI_NOTICE_MESSAGE = """
[
	{
		'type': 'section',
		'text': {
			'type': 'mrkdwn',
			'text': '*<%(URL)s|%(name)s>* 시작까지 *%(remain)s* 남았습니다.'
		}
	},
    {
        'type': 'context',
        'elements': [
			{
				'type': 'mrkdwn',
				'text': '시작시각 : %(datetime)s'
			}
		]
	},
	{
		'type': 'divider'
    }
]
"""

CANCELED_NOTICE_TXT = '%(name)s 취소되었습니다.'
CANCELED_NOTICE_MESSAGE = """
[
	{
		'type': 'section',
		'text': {
			'type': 'mrkdwn',
			'text': '*%(name)s* 대회가 취소되었습니다. :blobbandage:'
		}
	},
	{
		'type': 'divider'
    }
]
"""


SUBSCRIBE_KEYWORD = '!구독'
UNSUBSCRIBE_KEYWORD = '!구독해제'

NO_SUCH_USER = '그러한 유저가 존재하지 않습니다.'
ALREADY_EXISTS = '이미 목록에 추가된 유저입니다.'
APPEND_SUCCESS = '구독에 추가해 드렸습니다.'
DELETE_SUCCESS = '구독에서 제거해 드렸습니다.'