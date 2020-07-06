class Collector:
    """
    크롤링 클래스입니다.
    run 함수 호출 시, 비동기적으로 일정 주기로 크롤링합니다.
    크롤링이 완료될 때마다, update_call_back을 호출합니다.
    update_call_back은 다음과 같은 형태를 가져야 합니다.

    def call_back(contests: Iterable):
        pass

    Args:
        event_loop: 봇의 이벤트 루프
        update_call_back: collect 완료 시, 호출하는 콜백입니다.
    """

    _UPDATE_INTERVAL = 60 * 5  # 5분 간격으로 확인 예약

    def __init__(self, event_loop, update_call_back):
        self.event_loop = event_loop
        self.update_call_back = update_call_back
        self.stopped = False

    async def collect(self):
        raise NotImplementedError

    def run(self):
        """
        컬렉터를 가동합니다.
        정해진 업데이트 주기마다, collect 함수를 예약합니다.
        """
        self.stopped = False
        self._impl_run()

    def _impl_run(self):
        """
        run 함수의 구현부입니다.
        """
        if self.stopped:
            return

        self.event_loop.create_task(self.collect())
        self.event_loop.call_later(self._UPDATE_INTERVAL, self.run)

    def stop(self):
        """
        컬렉터의 가동을 멈춥니다.
        """
        self.stopped = True


class CollectManager:
    """
    콜렉터들의 관리 클래스입니다.
    완성된 컬렉터들을 일일히 구동할 필요없이
    한번에 모아서 관리해줍니다.
    """

    collector_list = []

    @staticmethod
    def register(collector: Collector):
        """
        CollectManger에 컬랙터를 등록합니다.
        """
        CollectManager.collector_list.append(collector)
        return collector

    def __init__(self, event_loop, update_call_back):
        self.event_loop = event_loop
        self.update_call_back = update_call_back

    def run(self):
        """
        등록된 컬렉터들을 작동시킵니다.
        """
        for collector in self.collector_list:
            collector.run()

    def stop(self):
        """
        등록된 컬렉터들에게 정지를 요청합니다.
        """
        for collector in self.collector_list:
            collector.stop()

