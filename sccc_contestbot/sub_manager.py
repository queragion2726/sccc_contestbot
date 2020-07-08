import logging
import functools

from sccc_contestbot.models import Subscriber


class AleadyExistsEception(Exception):
    pass


class NoSuchUserException(Exception):
    pass


class SubManager:
    """
    구독자를 관리합니다.
    봇 실행 이외에 단독으로 실행할 수는 없습니다.
    직접 생성하지 마세요.

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

    def __init__(self, event_loop, thread_local_data):
        self.event_loop = event_loop
        self.thread_local_data = thread_local_data

    async def add_subscriber(self, token):
        """
        토큰에 해당하는 유저를 구독자로 추가합니다.

        raises:
            AlreadyExistsException :
                이미 구독자 목록에 존재하는 유저를 추가할 경우
                이 예외를 발생시킵니다.
        """

        def _impl(thread_local_data):
            session = thread_local_data.Session()
            query = session.query(Subscriber).filter(Subscriber.token == token)

            if query.first() is not None:
                # 쿼리 결과가 존재한다면,
                session.close()
                raise AleadyExistsEception()
            else:
                session.add(Subscriber(token=token))
                session.commit()
            session.close()

        _impl = functools.partial(_impl, self.thread_local_data)

        try:
            await self.event_loop.run_in_executor(executor=None, func=_impl)
        except:
            raise

    async def delete_subscriber(self, token):
        """
        토큰에 해당하는 구독자를 삭제합니다.

        raises:
            NoSuchUserException : 지우려고하는 유저가
                구독 목록에 존재하지 않을경우 발생합니다.
        """

        def _impl(thread_local_data):
            session = thread_local_data.Session()
            query = session.query(Subscriber).filter(Subscriber.token == token)

            if query.first() is not None:
                # 쿼리 결과가 존재한다면,
                query.delete()
                session.commit()
            else:
                session.close()
                raise NoSuchUserException()

            session.close()

        _impl = functools.partial(_impl, self.thread_local_data)

        try:
            await self.event_loop.run_in_executor(executor=None, func=_impl)
        except:
            raise

    async def get_subscriber(self):
        """
        구독자들의 목록을 반환합니다.
        
        Returns:
            구독자 토큰(str)의 제너레이터를 반환합니다. 
        """

        def _impl(thread_local_data):
            session = thread_local_data.Session()
            query = session.query(Subscriber)
            results = (sub.token for sub in query.all())
            session.close()

            return results

        _impl = functools.partial(_impl, self.thread_local_data)

        return await self.event_loop.run_in_executor(executor=None, func=_impl)

