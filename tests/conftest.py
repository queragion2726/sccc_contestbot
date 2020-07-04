import os

import pytest
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker


from sccc_contestbot import ContestBot
from sccc_contestbot.models import Subscriber, Contest


@pytest.fixture
def bot():
    """
    테스트용으로 옵션을 설정한 봇을 생성합니다.
    """

    from app import parse_settings

    settings = parse_settings()
    settings["BOT_DB_HOST"] = "db-for-test"
    bot = ContestBot(**settings)

    # 테스트 디비의 테이블을 모두 비웁니다.
    Session = scoped_session(sessionmaker(bind=bot.engine))
    session = Session()
    session.query(Subscriber).delete()
    session.query(Contest).delete()
    session.commit()
    session.close()
    Session.remove()

    # 몇몇 DB 관련 클래스들은 활성화된 ThreadPoolExecutor를
    # 요구합니다.
    with bot.thread_pool_executor as pool:
        bot.event_loop.set_default_executor(pool)
        yield bot


@pytest.fixture
def db_session(bot):
    """
    데이터 베이스 세션을 얻어옵니다.
    """
    Session = scoped_session(sessionmaker(bind=bot.engine))
    session = Session()
    yield session
    session.close()
    Session.remove()


@pytest.fixture
def sub_manager(bot):
    return bot.sub_manager


@pytest.fixture
def event_loop(bot):
    return bot.event_loop
