from datetime import datetime, timedelta
from sccc_contestbot.time_strategy import TimeStrategy
from enum import Enum

# 타임존
LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo
# 포스팅할 채널을 의미합니다.
POST_CHANNEL = "#dev-playground"


class NOTI_STRATEGIES(Enum):
    # Notification strategies
    # 알림 주기를 설정합니다.
    # END 변수는 중요한 역할을 하니 삭제하지 마세요!
    END = TimeStrategy("for remove", seconds=0)
    BEFORE_10MINUTES = TimeStrategy(displayText="10분", minutes=10)
    BEFORE_1HOURS = TimeStrategy(displayText="1시간", hours=1)
    BEFORE_3HOURS = TimeStrategy(displayText="3시간", hours=3)
    BEFORE_1DAYS = TimeStrategy(displayText="하루", days=1)


# NOTICE_TXT will be displayed on app notification, not message.
# NOTICE_MESSAGE will be displayed message you know.
# NOTE: NOTICE_MESSAGE should be blocks format. Please check on slack api pages.
# https://api.slack.com/block-kit
# You can use some formatting to represent the contest information.
# %(name)s : contest name
# %(datetime)s : start datetime of contest
# %(remain)s : remaining time; value of TimeStrategy.dispalayText
# %(URL)s : URL of contest page

NEW_NOTICE_TXT = "%(name)s 등록되었습니다!"
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

MODIFIED_NOTICE_TXT = "%(name)s 일정이 변경되었습니다."
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

NOTI_NOTICE_TXT = "%(name)s %(remain)s 전!"
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

CANCELED_NOTICE_TXT = "%(name)s 취소되었습니다."
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


SUBSCRIBE_KEYWORD = "!구독"
UNSUBSCRIBE_KEYWORD = "!구독해제"

NO_SUCH_USER = "구독 목록에 존재하지 않습니다."
ALREADY_EXISTS = "이미 목록에 추가된 유저입니다."
APPEND_SUCCESS = "구독에 추가해 드렸습니다."
DELETE_SUCCESS = "구독에서 제거해 드렸습니다."

HELP_KEYWORD = "!도움말"
HELP_DISPLAY_TXT = "봇 도움말"
HELP_MESSAGE = f"""
*대회 알리미 슬랙 봇* : <https://github.com/queragion2726/sccc_contestbot|깃헙 링크>
구독하려면 채팅창에 "{SUBSCRIBE_KEYWORD}" 를 입력하세요.
반대로 구독해제는 "{UNSUBSCRIBE_KEYWORD}" 를 입력하세요.

구독시 대회 알림마다 태그 알림을 받을 수 있습니다.
"""

