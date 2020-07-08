# sccc_contestbot

대회 알리미 슬랙 봇

![Capture](img/Capture.jpg?raw=true)


## 빌드

```sh
git clone https://github.com/queragion2726/sccc_contestbot.git
cd sccc_contestbot
docker-compose build
```


## 기본 설정


```sh
vim settings.py
```

`settings.py` 에서 봇 관련 여러가지 사항들 (포스팅 채널, 메시지 포맷 등)을 수정할 수 있습니다.
자세한 사항은 `settings.py` 내부를 참조하세요

```sh
mkdir secrets
vim secrets/db_password.txt
vim secrets/slack_token.txt
```

내부 디비에서 사용할 패스워드와 slack_token을 설정합니다.


## 실행 Run

```sh
docker-compose up -d
```

## 개발

개발을 위한 도커파일은 `/docker-dev` 에 위치하고 있습니다

의존성 관리는 poetry 를 이용해 관리 중입니다.
