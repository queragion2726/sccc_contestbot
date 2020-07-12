from datetime import datetime

import pytest
from unittest.mock import MagicMock
from pytz import utc

from sccc_contestbot.models import Contest, ContestData
from sccc_contestbot.contest_manager import RenewalFlag
from .conftest import temp_db_data


def test_renewal_contest(contest_manager, db_session, event_loop):
    """
    renewal_contest 테스트
    """

    # renewal_call_back을 임시로 Mock로 바꿉니다.
    temporary_call_back = contest_manager.renewal_call_back
    # 컨테스트 추가 테스트
    contest_manager.renewal_call_back = MagicMock()

    test_contest = ContestData("A", "A", datetime.now(utc), "A")

    event_loop.run_until_complete(contest_manager.renewal_contest(test_contest))
    contest_manager.renewal_call_back.assert_called_with(
        test_contest, RenewalFlag.CREATED
    )
    assert (
        db_session.query(Contest).filter(Contest.contest_id == "A").first() is not None
    )

    # 똑같은 컨테스트 중복 테스트

    contest_manager.renewal_call_back = MagicMock()
    event_loop.run_until_complete(contest_manager.renewal_contest(test_contest))
    assert not contest_manager.renewal_call_back.called

    # 콘테스트 변경 테스트
    new_contest = ContestData("A", "B", datetime.now(utc), "BB")
    event_loop.run_until_complete(contest_manager.renewal_contest(new_contest))
    contest_manager.renewal_call_back.assert_called_with(
        new_contest, RenewalFlag.CHANGED
    )

    db_session.query(Contest).filter(Contest.contest_id == "A").delete()
    db_session.commit()
    db_session.close()

    contest_manager.renewal_call_back = temporary_call_back


def test_delete_contest(contest_manager, db_session, event_loop):
    """
    콘테스트 삭제 테스트
    """

    test_data = ContestData("A", "A", datetime.now(utc), "A")

    # 데이터가 없으니 삭제되지 않고, 예외도 뜨면 안된다.
    event_loop.run_until_complete(contest_manager.delete_contest(test_data))

    with temp_db_data(db_session, (Contest(test_data),)):
        event_loop.run_until_complete(contest_manager.delete_contest(test_data))
        assert (
            db_session.query(Contest).filter(Contest.contest_id == "A").first() is None
        )


def test_is_latest(contest_manager, db_session_maker, event_loop):
    """
    특정한 콘테스트가 최신인지 확인하는 기능을 테스트합니다.
    """
    test_contest = ContestData("ID", "A", datetime.now(utc), "B")
    assert False == event_loop.run_until_complete(
        contest_manager.is_latest(test_contest)
    )

    # 첫번째 세션, 콘테스트 추가 후, 검사
    db_session = db_session_maker()
    db_session.add(Contest(test_contest))
    db_session.commit()

    assert True == event_loop.run_until_complete(
        contest_manager.is_latest(test_contest)
    )

    db_session.close()

    # 두번째 세션, 콘테스트 변경 후, 검사
    db_session = db_session_maker()

    changed_contest = ContestData("ID", "AA", datetime.now(utc), "BB")
    db_session.query(Contest).filter(Contest.contest_id == "ID").update(
        {
            Contest.contest_name: changed_contest.contest_name,
            Contest.start_date: changed_contest.start_date,
            Contest.URL: changed_contest.URL,
            Contest.hash_value: changed_contest.hash_value,
        }
    )
    db_session.commit()

    assert test_contest.contest_name != changed_contest.contest_name

    assert False == event_loop.run_until_complete(
        contest_manager.is_latest(test_contest)
    )

    db_session.query(Contest).filter(Contest.contest_id == "ID").delete()
    db_session.commit()
    db_session.close()
