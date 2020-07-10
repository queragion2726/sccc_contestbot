# sccc_contestbot

대회 알리미 슬랙 봇

![Capture](img/Capture.jpg?raw=true)


## 레포지토리 클론

```sh
git clone https://github.com/queragion2726/sccc_contestbot.git
cd sccc_contestbot
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

```sh
chmod 440 secrets/db_password.txt
chmod 440 secrets/slack_token.txt
```

크게 상관은 없습니다만, 다른 유저의 읽기 권한을 없애주셔도 됩니다.

## 빌드 

```sh
docker-compose build
```

## 실행 

```sh
docker-compose up -d
```

## 개발

개발을 위한 도커파일은 `/docker-dev` 에 위치하고 있습니다

의존성 관리는 poetry 를 이용해 관리 중입니다.

개발용 참고사항:

- 개발용 도커파일은 디비서버를 총 두개 생성합니다. 하나는 테스트용 서버(pytest 이용시 사용하는 서버), 봇 서버 입니다.
- 이 중 테스트용 서버는 따로 볼륨이 존재하지 않아, 재시작 시 모든 내용이 초기화 됩니다.
- 봇의 /app 디렉토리는 프로젝트 디렉토리로 bind mount 되어 있습니다.

