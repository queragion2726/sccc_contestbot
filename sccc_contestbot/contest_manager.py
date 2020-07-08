import functools
import asyncio
from enum import Enum

from sccc_contestbot.models import Contest, ContestData


class RenewalFlag(Enum):
    CREATED = 1
    CHANGED = 2


class ContestManager:
    """
    컨테스트를 관리합니다.
    봇 실행 이외에 단독으로 실행할 수는 없습니다.
    직접 생성하지 마세요.

    Args:
        renewal_call_back :
            컨테스트 갱신시, 새로 추가되었거나 바뀐사항이 있을 경우
            이 콜백을 호출합니다.
            콜백은 다음과 같은 꼴을 만족해야합니다.
            def renewal_call_back(contest:Contest, flag:RenewalFlag)

    참고:
        sqlalchemy의 API는 block을 유발하기 때문에,
        ThreadPoolExecutor을 사용해 별도의 스레드에서 관리합니다.

        이 때문에, ContestBot 클래스의 run 메서드에 강하게 종속적입니다.
        세가지 코드에 종속성이 있습니다.
        - self.thread_pool_executor = ThreadPoolExecutor( ... )
            스레드 내부에 scopped_session을 만드는 작업이 필요합니다.
        - with self.thread_pool_executor as pool: ...
            ThreadPoolExecutor의 context가 활성화 상태여야 합니다.
        - loop.set_default_executor(pool)
            이벤트 루프의 기본 executor가 활성화된 상태의 
            ThreadPoolExecutor 이어야 합니다.
            loop.run_in_executor(executor=None ... )은
            디폴트 executor을 실행시킨다는걸 주의하세요!
    """

    def __init__(self, event_loop, thread_local_data, renewal_call_back):
        self.event_loop = event_loop
        self.thread_local_data = thread_local_data
        self.renewal_call_back = renewal_call_back
        self.lock = asyncio.Lock()

    async def renewal_contest(self, contest: ContestData):
        """
        데이터베이스에 컨테스트를 추가하거나 갱신합니다.
        만약 동일한 컨테스트가 이미 존재할경우, 아무것도 하지 않습니다.

        새로 추가되었거나 갱신했을 경우, 미리 지정한 콜백을 호출합니다.

        """

        def _impl(thread_local_data):
            session = thread_local_data.Session()
            item = (
                session.query(Contest)
                .filter(Contest.contest_id == contest.contest_id)
                .first()
            )

            if item is None:
                session.add(Contest(contest))
                session.commit()
                session.close()
                return RenewalFlag.CREATED

            if item.hash_value != contest.hash_value:
                setattr(item, "contest_name", contest.contest_name)
                setattr(item, "start_date", contest.start_date)
                setattr(item, "URL", contest.URL)
                setattr(item, "hash_value", contest.hash_value)
                session.commit()
                session.close()
                return RenewalFlag.CHANGED

            # Non changed
            session.close()
            return None

        _impl = functools.partial(_impl, self.thread_local_data)

        async with self.lock:
            result_flag = await self.event_loop.run_in_executor(
                executor=None, func=_impl
            )

        if result_flag is None:
            pass
        else:
            self.renewal_call_back(contest, result_flag)

    async def delete_contest(self, contest: ContestData):
        """
        해당하는 콘테스트가 존재한다면 제거합니다.
        콘테스트가 존재하지 않아도 예외를 발생시키지는 않습니다.

        주의:
            콘테스트를 제거하는 키 값은 contest_id 를 기준으로 합니다.
        """

        def _impl(thread_local_data):
            session = thread_local_data.Session()
            session.query(Contest).filter(
                Contest.contest_id == contest.contest_id
            ).delete()
            session.commit()
            session.close()

        _impl = functools.partial(_impl, self.thread_local_data)

        async with self.lock:
            await self.event_loop.run_in_executor(executor=None, func=_impl)

    async def is_latest(self, contest: ContestData) -> bool:
        """
        이 콘테스트 객체가, 최신정보인지 확인합니다.

        returns:
            최신정보와 동일하다면 True, 아니면 False를 반환합니다.
        """

        def _impl(thread_local_data):
            session = thread_local_data.Session()
            hash_value = (
                session.query(Contest.hash_value)
                .filter(Contest.contest_id == contest.contest_id)
                .scalar()
            )
            session.close()

            if hash_value is None:
                return False

            return hash_value == contest.hash_value

        _impl = functools.partial(_impl, self.thread_local_data)

        return await self.event_loop.run_in_executor(executor=None, func=_impl)
