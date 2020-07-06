import asyncio
import logging
import threading
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

import slack
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

import settings
from .models import Base, Contest, Subscriber, ContestData
from .sub_manager import SubManager
from .contest_manager import ContestManager, RenewalFlag
from sccc_contestbot.collectors import CollectManager


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
            DB_ENGINE : sqlalchemy 엔진을 직접 생성한 경우,
                인자로 넘겨 줄 수 있습니다. 주로 테스트를 위해
                사용합니다.
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

        slack.RTMClient.run_on(event="message")(self.message_listener)

        logger.info("슬랙 클라이언트 초기화 완료")

        # DB 엔진 초기화
        if "DB_ENGINE" in kwargs:
            self.engine = kwargs["DB_ENGINE"]
        else:
            self.engine = sqlalchemy.create_engine(
                "postgresql://{}:{}@{}:{}/{}".format(
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

        # DB API 처리를 위한 Bot만의 ThreadPoolExecutor 생성

        # 스레드 별 DB 세션 생성을 위한 initializer
        # 각 스레드는 스레드만의 scoped_session을 가지게 된다.
        self.thread_local_data = threading.local()

        def thread_session_maker(thread_local_data, engine):
            thread_local_data.Session = scoped_session(sessionmaker(bind=engine))

        self.thread_pool_executor = ThreadPoolExecutor(
            initializer=thread_session_maker,
            initargs=(self.thread_local_data, self.engine),
        )

        # 구독자 관리자 생성

        self.sub_manager = SubManager(self.event_loop, self.thread_local_data)

        # 콘테스트 관리자 생성

        self.contest_manager = ContestManager(
            self.event_loop, self.thread_local_data, self.renewal_call_back
        )

        # 컬렉터 관리자 생성

        self.collect_manager = CollectManager(
            self.event_loop, self.contest_update_call_back
        )

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
        loop = self.event_loop

        # 크롤링 시작 예약
        self.collect_manager.run()

        rtm_client_future = self.rtm_client.start()

        try:
            with self.thread_pool_executor as pool:
                # 루프의 기본 실행자를 pool로 설정합니다
                loop.set_default_executor(pool)
                loop.run_until_complete(rtm_client_future)
        finally:
            loop.close()

    def renewal_call_back(self, contest: Contest, flag: RenewalFlag):
        pass

    def contest_update_call_back(self, contests: List[ContestData]):
        pass

    async def message_listener(self, **payload):
        """
        슬랙 채널에서 받아온 메시지들을 분류해 처리합니다.
        """
        data = payload["data"]

        if "user" in data:
            # 유저의 메시지
            if settings.SUBSCRIBE_KEYWORD == data["txt"]:
                # 구독자 등록
                await self.add_subscriber(**payload)
            elif settings.UNSUBSCRIBE_KEYWORD == data["txt"]:
                # 구독자 제거
                await self.delete_subscriber(**payload)
            elif settings.HELP_KEYWORD == data["txt"]:
                # 도움말 메시지
                await self.post_help_message(**payload)
            elif "!TEST" == data["txt"]:
                # 테스트용
                await self.post_test_message(**payload)
        if (
            "subtype" in data
            and data["subtype"] == "bot_message"
            and "thread_ts" not in data
            and "blocks" in data
        ):
            # 구독자에게 알림을 보내줘야하는 메시지를 판단합니다.
            if data["text"] == settings.HELP_DISPLAY_TXT:
                return
            await self.post_subscriber(**payload)

    async def add_subscriber(self, **payload):
        pass

    async def delete_subscriber(self, **payload):
        pass

    async def post_help_message(self, **payload):
        pass

    async def post_test_message(self, **payload):
        pass

    async def post_subscriber(self, **payload):
        pass

