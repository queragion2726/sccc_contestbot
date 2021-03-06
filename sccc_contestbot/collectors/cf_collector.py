import json
import logging
from datetime import datetime

import aiohttp
from pytz import utc

from settings import LOCAL_TIMEZONE
from sccc_contestbot.models import ContestData
from . import Collector, CollectManager

logger = logging.getLogger(__name__)


class CodeforcesData(ContestData):
    def __init__(self, id_value: int, name, start_time):
        super().__init__(
            "CF" + str(id_value),
            name,
            datetime.fromtimestamp(start_time, utc),
            f"http://codeforces.com/contests/{str(id_value)}",
        )


class CFCollector(Collector):
    _TARG_URL = "http://codeforces.com/api/contest.list?gym=false&lang=en"

    async def collect(self):
        ret = []
        attempt_count = 0
        while True:
            attempt_count += 1
            try:
                async with aiohttp.ClientSession(raise_for_status=True) as session:
                    async with session.get(self._TARG_URL) as resp:
                        txt = await resp.text()

                        contest_list = json.loads(txt)["result"]
                        for contest in contest_list:
                            if contest["phase"] != "BEFORE":
                                break
                            data = CodeforcesData(
                                contest["id"],
                                contest["name"],
                                contest["startTimeSeconds"],
                            )
                            ret.append(data)
                break
            except aiohttp.ClientError as e:
                logger.error("CF", exc_info=e)
                await self.error_wait(attempt_count)
                continue
            except Exception as e:
                logger.error("CF : 알수없는 에러", exc_info=e)
                await self.error_wait(attempt_count)
                continue
        self.update_call_back(ret)
