import asyncio
import logging
import sys
import time

import slack
import sqlalchemy


def init_logger(mod_name):
    """
    모듈별 로거를 생성합니다.
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)-8s: [%(name)s] : %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


init_logger(__name__)
logger = logging.getLogger(__name__)


class ContestBot:
    def __init__(self, **kwargs):
        """
        봇 초기화

        Args:
            BOT_SLACK_TOKEN : slack bot api token이 필요합니다.
            BOT_DB_HOST :
            BOT_DB_PORT :
            BOT_DB_NAME :
            BOT_DB_USERNAME :
            BOT_DB_PASSWORD : 
        """
        # TODO: 파라미터 설명 보충
        logger.info("---콘테스트 봇 초기화---")

        # Slack client 초기화
        token = kwargs["BOT_SLACK_TOKEN"]

        self.event_loop = asyncio.get_event_loop()
        self.rtm_client = slack.RTMClient(
            token=token, run_async=True, loop=self.event_loop
        )
        self.web_client = slack.WebClient(
            token=token, run_async=True, loop=self.event_loop
        )
        logger.info("슬랙 봇 초기화 완료")

        # DB 엔진 초기화
        self.engine = sqlalchemy.create_engine(
            "postgres://{}:{}@{}:{}/{}".format(
                kwargs["BOT_DB_USERNAME"],
                kwargs["BOT_DB_PASSWORD"],
                kwargs["BOT_DB_HOST"],
                kwargs["BOT_DB_PORT"],
                kwargs["BOT_DB_NAME"],
            )
        )
        logger.info("DB 엔진 생성 완료")

        # TODO: 파서 추가

    def run(self, db_try_connection_count=5):
        """
        봇을 실행합니다.

        args:
            db_try_connection_count: 최대 이 횟수만큼 DB에 연결을 시도합니다.
        """

        # DB 커넥션 대기
        logger.info("DB 커넥트 대기 중")
        try_count = 0
        while True:
            try:
                self.engine.execute("select 1")
                break
            except RuntimeError:
                logger.info("연결 실패...")
                time.sleep(min(10 * 1000, 2 ** (try_count + 6)))
                try_count += 1

            if try_count == db_try_connection_count:
                break

        logger.info("DB 커넥션 성공")

