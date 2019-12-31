from datetime import datetime

LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo

POST_CHANNEL = '#dev-playground'

# NOTICE_TXT will be displayed on app notification, not message.
# NOTICE_MESSAGE will be displayed like normal message you know.
# NOTE: NOTICE_MESSAGE should be blocks format
# https://api.slack.com/block-kit

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
