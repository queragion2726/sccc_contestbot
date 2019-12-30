from datetime import datetime

LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo

POST_CHANNEL = '#random'

NEW_NOTICE_MESSAGE = dict()
NEW_NOTICE_MESSAGE['pretext'] = '*새 대회가 추가되었습니다!!* :blobaww: :blobaww:'
NEW_NOTICE_MESSAGE['title'] =  '{name}'
NEW_NOTICE_MESSAGE['title_link'] =  '{URL}'
NEW_NOTICE_MESSAGE['text'] = '{date}'

MODIFIED_NOTICE_MESSAGE = dict()
MODIFIED_NOTICE_MESSAGE['pretext'] = '*대회 일정이 변경되었습니다...* :blobsob:'
MODIFIED_NOTICE_MESSAGE['title'] =  '{name}'
MODIFIED_NOTICE_MESSAGE['title_link'] =  '{URL}'
MODIFIED_NOTICE_MESSAGE['text'] = '{date}'

NOTI_NOTICE_MESSAGE = dict()
NOTI_NOTICE_MESSAGE['pretext'] = '*<{URL}|{name}> 시작까지 약 {remain} 남았습니다!*'
NOTI_NOTICE_MESSAGE['title'] =  '{name}'
NOTI_NOTICE_MESSAGE['title_link'] =  '{URL}'
NOTI_NOTICE_MESSAGE['text'] = '{date}'
