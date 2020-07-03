import asyncio
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor

import pytest

from sccc_contestbot.models import Subscriber


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

    for data in datas:
        db_session.delete(data)
    db_session.commit()


def test_get_subscriber(bot, db_session):
    """
    구독자 얻어오기 테스트
    """

    sub_manager = bot.sub_manager

    with temp_db_data(
        db_session, (Subscriber(token="Test1"), Subscriber(token="Test2"),)
    ):
        loop = bot.event_loop
        result = loop.run_until_complete(sub_manager.get_subscriber())

    result = list(result)
    assert result == ["Test1", "Test2"]

