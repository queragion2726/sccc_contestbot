# sccc_contestbot

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.6%20|%203.7-blue">
    <img src="https://img.shields.io/badge/License-Apache--2.0-blue">
</p>

대회 알리미 슬랙 봇

Slack bot noticing contest informations.

![Capture](img/Capture.jpg?raw=true)

## 요구사항

- Python3.6 or upper
- aiohttp, slackclient


## 설치 Installation

필요한 모듈이 없다면, 설치해주세요.

Please, install required modules if you don't have

```sh
pip3 install aiohttp 
pip3 install slackclient
```

## 사용법 Usage

```sh
git clone https://github.com/queragion2726/sccc_contestbot.git
cd sccc_contestbot
```

```sh
vim settings.py
```

`settings.py` 에서 봇 관련 여러가지 사항들 (포스팅 채널, 메시지 포맷 등)을 수정할 수 있습니다.

You can change several options about bots (channel to post, message format, etc.) on `settings.py`

파일을 참고하세요.

Please, check on the file.

## 실행 Run

```sh
# SLACK_API_TOKEN='xoxb-xxxx....'
env SLACK_API_TOKEN='{your slack api token}' python3 run.py
```

