import os

import pytest

from sccc_contestbot import ContestBot


@pytest.fixture
def bot():
    """
    테스트용으로 옵션을 설정한 봇을 생성합니다.
    """

    from app import parse_settings

    settings = parse_settings()
    bot = ContestBot(**settings)

    return bot

