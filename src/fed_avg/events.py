from src.fed_avg.constant import AGGREGATE_TEST_DONE
from src.base.states.event import Event


class AggregateModelTestDone(Event):
    def __init__(self, round_id: int):
        super(AggregateModelTestDone, self).__init__(AGGREGATE_TEST_DONE)
        self.round_id = round_id
