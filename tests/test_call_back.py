from datetime import datetime, timedelta
from pytz import utc

from sccc_contestbot.models import ContestData
from sccc_contestbot.contest_manager import RenewalFlag

import settings


def test_renewal_call_back(monkeypatch, bot):
    """
    renewal_call_back이 제대로 작동하는지 확인합니다.
    """
    # 현재시각으로부터 이틀 후
    new_test_time = datetime.now(tz=settings.LOCAL_TIMEZONE) + timedelta(days=2)
    new_test_ID = "ID"
    new_test_name = "NAME"
    new_test_URL = "URL"
    test_contest = ContestData(new_test_ID, new_test_name, new_test_time, new_test_URL)

    result_list = []

    def fake_call_later(delay, callback, contest, time_strategy):
        """
        arguments들을 result_list에 저장합니다.
        """
        result_list.append((contest, time_strategy,))

    def fake_chat_postMessage(**kwargs):
        assert kwargs["channel"] == settings.POST_CHANNEL
        assert kwargs["text"] == f"{new_test_name} {str(new_test_time)} {new_test_URL}"
        assert "blocks" in kwargs

    monkeypatch.setattr(bot.event_loop, "call_later", fake_call_later)
    monkeypatch.setattr(bot.web_client, "chat_postMessage", fake_chat_postMessage)

    monkeypatch.setattr(settings, "NEW_NOTICE_TXT", "%(name)s %(datetime)s %(URL)s")
    monkeypatch.setattr(
        settings, "MODIFIED_NOTICE_TXT", "%(name)s %(datetime)s %(URL)s"
    )

    # CREATED 테스트
    result_list = []
    bot.renewal_call_back(test_contest, RenewalFlag.CREATED)

    for item in settings.NOTI_STRATEGIES:
        assert (test_contest, item.value,) in result_list

    # CHANGED 테스트
    result_list = []
    bot.renewal_call_back(test_contest, RenewalFlag.CHANGED)
    for item in settings.NOTI_STRATEGIES:
        assert (test_contest, item.value,) in result_list

