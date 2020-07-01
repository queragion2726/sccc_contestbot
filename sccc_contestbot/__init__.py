import asyncio
import logging
import sys
import time

import slack
import sqlalchemy

from .models import Base


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
        logger.info("------콘테스트 봇 초기화------")

        # Slack client 초기화
        token = kwargs["BOT_SLACK_TOKEN"]

        self.event_loop = asyncio.get_event_loop()
        self.rtm_client = slack.RTMClient(
            token=token, run_async=True, loop=self.event_loop
        )
        self.web_client = slack.WebClient(
            token=token, run_async=True, loop=self.event_loop
        )
        logger.info("슬랙 클라이언트 초기화 완료")

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
        if not self.test_db(self.engine):
            Base.metadata.create_all(self.engine)
            logger.info("테이블 생성을 완료했습니다.")
        logger.info("DB 엔진 생성 완료")

        # TODO: 파서 추가

    def test_db(self, engine, connect_try_count=5) -> bool:
        """
        DB 커넥션을 테스트해보고,
        만약 테이블이 작성되지 않았을 경우 False를 반환합니다.
        """

        # DB 커넥션 대기
        logger.info("DB 커넥트 대기 중")
        try_count = 0
        while True:
            try:
                self.engine.execute("SELECT 1")
                break
            except sqlalchemy.exc.DatabaseError:
                logger.info("연결 실패...")
                time.sleep(min(10, 0.001 * (2 ** (try_count + 7))))
                try_count += 1

            if try_count == connect_try_count:
                raise RuntimeError("DB 연결 실패")
        logger.info("DB 커넥션 성공")

        logger.info("contests 테이블이 존재하는지 확인합니다.")
        try:
            self.engine.execute("SELECT * FROM contests")
            logger.info("정상적으로 존재합니다.")
        except sqlalchemy.exc.ProgrammingError:
            logger.info("존재하지 않습니다. 테이블을 생성합니다.")
            return False

        return True

    def run(self):
        """
        봇을 실행합니다.
        """

