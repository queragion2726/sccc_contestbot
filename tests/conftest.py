import os

import pytest
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker


from sccc_contestbot import ContestBot


@pytest.fixture
def bot():
    """
    테스트용으로 옵션을 설정한 봇을 생성합니다.
    """

    from app import parse_settings

    settings = parse_settings()
    settings["BOT_DB_HOST"] = "db-for-test"
    bot = ContestBot(**settings)

    # 몇몇 DB 관련 클래스들은 활성화된 ThreadPoolExecutor를
    # 요구합니다.
    with bot.thread_pool_executor as pool:
        bot.event_loop.set_default_executor(pool)
        yield bot

    bot.event_loop.close()


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
