import asyncio
from concurrent.futures import ThreadPoolExecutor

import pytest
import sqlalchemy

from sccc_contestbot.models import Subscriber
from sccc_contestbot.sub_manager import AleadyExistsEception, NoSuchUserException
from .conftest import temp_db_data


def test_get_subscriber(sub_manager, event_loop, db_session):
    """
    구독자 얻어오기 테스트
    """

    with temp_db_data(
        db_session, (Subscriber(token="Test1"), Subscriber(token="Test2"),)
    ):
        result = event_loop.run_until_complete(sub_manager.get_subscriber())

    result = list(result)
    assert result == ["Test1", "Test2"]


def test_add_subscriber(sub_manager, event_loop, db_session):
    """
    구독자 추가 테스트
    """

    event_loop.run_until_complete(sub_manager.add_subscriber("Test1"))
    assert (
        db_session.query(Subscriber).filter(Subscriber.token == "Test1").first()
        is not None
    )

    with pytest.raises(AleadyExistsEception):
        event_loop.run_until_complete(sub_manager.add_subscriber("Test1"))

    # 테스트 때문에 추가된 row 삭제
    db_session.query(Subscriber).filter(Subscriber.token == "Test1").delete()


def test_delete_subscriber(sub_manager, event_loop, db_session):
    """
    구독자 제거 테스트
    """

    with temp_db_data(db_session, (Subscriber(token="Test"),)):
        event_loop.run_until_complete(sub_manager.delete_subscriber("Test"))

    with pytest.raises(NoSuchUserException):
        event_loop.run_until_complete(sub_manager.delete_subscriber("Test"))


def test_add_delete_subscriber(sub_manager, event_loop, db_session):
    event_loop.run_until_complete(sub_manager.add_subscriber("Test!!"))
    event_loop.run_until_complete(sub_manager.delete_subscriber("Test!!"))

    assert (
        db_session.query(Subscriber).filter(Subscriber.token == "Test!!").first()
        is None
    )

