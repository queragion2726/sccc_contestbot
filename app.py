import os

import sqlalchemy

from sccc_contestbot import ContestBot


def parse_settings() -> dict:
    """
    봇 세팅에 필요한 여러 옵션을 가져옵니다.
    """
    ret = dict()

    try:
        ret["BOT_DB_NAME"] = os.environ["BOT_DB_NAME"]
        ret["BOT_DB_USERNAME"] = os.environ["BOT_DB_USERNAME"]
        ret["BOT_DB_HOST"] = os.environ["BOT_DB_HOST"]
        ret["BOT_DB_PORT"] = os.environ["BOT_DB_PORT"]
    except KeyError as e:
        raise RuntimeError(f"환경변수 {str(e)}가 존재하지 않습니다.")

    ret["BOT_DB_PASSWORD"] = os.environ.get("BOT_DB_PASSWORD")

    try:
        if ret["BOT_DB_PASSWORD"] is None:
            filename = os.environ["BOT_DB_PASSWORD_FILE"]
            with open(filename, "r") as password_file:
                ret["BOT_DB_PASSWORD"] = password_file.readline().strip()
    except KeyError as e:
        raise RuntimeError("DB 비밀번호와 관련된 환경변수가 존재하지 않습니다.")
    except FileNotFoundError as e:
        raise RuntimeError("비밀번호에 해당하는 파일을 찾을 수가 없습니다.")

    ret["BOT_SLACK_TOKEN"] = os.environ.get("BOT_SLACK_TOKEN")
    try:
        if ret["BOT_SLACK_TOKEN"] is None:
            filename = os.environ["BOT_DB_PASSWORD_FILE"]
            with open(filename, "r") as password_file:
                ret["BOT_SLACK_TOKEN"] = password_file.readline().strip()
    except KeyError as e:
        raise RuntimeError("슬랙 토큰과 관련된 환경변수가 존재하지 않습니다.")
    except FileNotFoundError as e:
        raise RuntimeError("슬랙토큰에 해당하는 파일을 찾을 수가 없습니다.")

    return ret


def main():
    settings = parse_settings()
    bot = ContestBot(**settings)

    bot.run()


if __name__ == "__main__":
    main()
