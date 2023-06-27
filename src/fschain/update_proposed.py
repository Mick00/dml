from src.base.states.event import Event
from src.fschain.constants import UPDATE_PROPOSED


class UpdateProposed(Event):
    def __init__(self, round_id: int, parent: str, updateId: int, proposer: str, uri: str ):
        super(UpdateProposed, self).__init__(UPDATE_PROPOSED)
        self.parent = parent
        self.updatesId = updateId
        self.proposer = proposer
        self.uri = uri