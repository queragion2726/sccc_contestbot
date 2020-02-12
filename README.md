# sccc_contestbot

주의: 아직 완성되지 않은 프로젝트입니다. 리드미도요.

NOTE: Not completed project, also README

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.6%20|%203.7-blue">
    <img src="https://img.shields.io/badge/License-Apache--2.0-blue">
</p>

대회 알리미 슬랙 봇

Slack bot noticing contest informations.


## 요구사항

- Python3.6 이상
- aiohttp, slackclient


## 설치 Installation

필요한 모듈이 없다면, 설치해주세요.

Please, install required modules if you don't have

```
$ pip3 install aiohttp 
$ pip3 install slackclient
```

그냥 클론하세요. Just clone this repository.
```
$ git clone https://github.com/queragion2726/sccc_contestbot.git
```

## 사용법 Usage

`settings.py` 에서 봇 관련 여러가지 사항들 (포스팅 채널, 메시지 포맷 등)을 수정할 수 있습니다.

You can change several options about bots (channel to post, message format, etc.) on `settings.py`

파일을 참고하세요.

Please, check on the file.


```
$ env SLACK_TOKEN='xoxb-xxxx...' python3 run.py &
```

