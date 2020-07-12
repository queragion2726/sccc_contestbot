import os
from contextlib import contextmanager

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
def db_session_maker(bot):
    """
    데이터 베이스 세션을 직접 관리하고 싶을 때
    직접 불러와 사용할 수 있습니다.
    """
    return scoped_session(sessionmaker(bind=bot.engine))


@pytest.fixture
def sub_manager(bot):
    return bot.sub_manager


@pytest.fixture
def contest_manager(bot):
    return bot.contest_manager


@pytest.fixture
def event_loop(bot):
    return bot.event_loop


@contextmanager
def temp_db_data(db_session, datas):
    """
    db_session에 해당하는 데이터를 넣습니다.
    이 데이터들은 context가 종료시 사라집니다.
    """
    for data in datas:
        db_session.add(data)
    db_session.commit()

    yield db_session

    # 데이터들을 삭제합니다.
    # context 내부에서 데이터가 삭제되었을 경우를 상정합니다.
    # 이미 삭제했을 경우 commit에서 예외가 발생 후 db_session.rollback 이 실행됩니다.
    # 이를 막고 처리합니다.
    db_session.commit()

    for data in datas:
        try:
            db_session.delete(data)
            db_session.commit()
        except:
            pass
