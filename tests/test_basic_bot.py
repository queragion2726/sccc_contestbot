import pytest

from sccc_contestbot import ContestBot
from app import parse_settings


def test_wrong_password():
    settings = parse_settings()
    settings["BOT_DB_PASSWORD"] += "123adsf"

    with pytest.raises(RuntimeError) as excinfo:
        ContestBot(**settings)

    assert "연결 실패" in str(excinfo)

