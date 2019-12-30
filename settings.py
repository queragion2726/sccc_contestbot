from datetime import datetime

LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo

POST_CHANNEL = '#dev-playground'

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
