from datetime import datetime
from timeStrategy import TimeStrategy
from enum import Enum
from codeforcesGetter import CodeforcesGetter

LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo

POST_CHANNEL = '#dev-playground'

class GETTERS(Enum):
    CODEFORCES = CodeforcesGetter

class NOTI_STRATEGIES(Enum):
    END = TimeStrategy("for remove", seconds=0)
    BEFORE_10MINUTES = TimeStrategy("10분 전", minutes=10)
    BEFORE_30MINUTES = TimeStrategy("30분 전", minutes=30)
    BEFORE_3HOURS = TimeStrategy("3시간 전", hours=3)

# NOTICE_TXT will be displayed on app notification, not message.
# NOTICE_MESSAGE will be displayed like normal message you know.
# NOTE: NOTICE_MESSAGE should be blocks format. Please check on slack api pages.
# https://api.slack.com/block-kit
# You can use some formatting to represent the contest information.
# {name} : contest name
# {datetime} : start datetime of contest
# {remain} : remaining time
# {URL} : URL of contest page

NEW_NOTICE_TXT = '{name} 등록되었습니다!'
NEW_NOTICE_MESSAGE = """[
    {{
		'type': 'section',
		'text': {{
			'type': 'mrkdwn',
			'text': '*<{URL}|{name}>*'
		}}
	}},
	{{
		'type': 'context',
		'elements': [
            {{
                'type': 'mrkdwn',
                'text': '*새로운 대회가 등록되었습니다!! *:blobaww:\n'
            }}
        ]
    }},
    {{
        'type': 'context',
        'elements': [
			{{
				'type': 'mrkdwn',
				'text': '시작시각 : {datetime}'
			}}
		]
	}},
	{{
		'type': 'divider'
	}}
]"""

MODIFIED_NOTICE_TXT = '{name} 일정이 변경되었습니다.'
MODIFIED_NOTICE_MESSAGE = """[
    {{
		'type': 'section',
		'text': {{
			'type': 'mrkdwn',
			'text': '*<{URL}|{name}>*'
		}}
	}},
	{{
		'type': 'context',
		'elements': [
            {{
                'type': 'mrkdwn',
                'text': '*대회 일정이 변경되었습니다... *:blobsob:\n'
            }}
        ]
    }},
    {{
        'type': 'context',
        'elements': [
			{{
				'type': 'mrkdwn',
				'text': '시작시각 : {datetime}'
			}}
		]
	}},
	{{
		'type': 'divider'
    }}
]
"""

NOTI_NOTICE_TXT = '{name} {remain} 전!'
NOTI_NOTICE_MESSAGE = """[
{{
		'type': 'section',
		'text': {{
			'type': 'mrkdwn',
			'text': '*<{URL}|{name}>* 시작까지 *{remain}* 남았습니다.'
		}}
	}},
    {{
        'type': 'context',
        'elements': [
			{{
				'type': 'mrkdwn',
				'text': '시작시각 : {datetime}'
			}}
		]
	}},
	{{
		'type': 'divider'
    }}
]
"""
