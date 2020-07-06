import re
import logging
from datetime import datetime, timezone

import aiohttp
from bs4 import BeautifulSoup

from settings import LOCAL_TIMEZONE
from sccc_contestbot import init_logger
from sccc_contestbot.models import ContestData
from . import Collector, CollectManager

init_logger(__name__)
logger = logging.getLogger(__name__)


class BaekjoonData(ContestData):
    def __init__(self, id_value: str, name, start_time):
        super().__init__(
            "BOJ" + id_value,
            name,
            start_time,
            f"https://www.acmicpc.net/contest/view/{id_value}",
        )


@CollectManager.register
class BOJCollector(Collector):
    _TARGET_URL = "https://www.acmicpc.net/contest/official/list"
    _UPDATE_INTERVAL = 60 * 60  # 1시간
    _RE_REPR = re.compile(r"\d+")

    async def collect(self):
        ret = []
        attempt_count = 0
        while True:
            attempt_count += 1
            try:
                async with aiohttp.ClientSession(raise_for_status=True) as session:
                    async with session.get(self._TARGET_URL) as resp:
                        req = await resp.text()
                        soup = BeautifulSoup(req, features="html.parser")

                        contest_list = soup.find_all("tr", {"class": "info"})
                        for contest in contest_list:
                            contents = contest.contents
                            id_value = contents[1].a.attrs["href"].split("/")[-1]
                            name = contents[1].a.text
                            start_time = contents[7].text
                            start_time = datetime(
                                *map(int, self._RE_REPR.findall(start_time)),
                                tzinfo=LOCAL_TIMEZONE,
                            )

                            if start_time < datetime.now(timezone.utc):
                                break

                            data = BaekjoonData(id_value, name, start_time)

                            ret.append(data)
                break
            except aiohttp.ClientError as e:
                logger.error("BOJ", exc_info=e)
                await self.error_wait(attempt_count)
                continue
            except Exception as e:
                logger.error("BOJ : 알수없는 에러", exc_info=e)
                await self.error_wait(attempt_count)
                continue
        self.update_call_back(ret)
