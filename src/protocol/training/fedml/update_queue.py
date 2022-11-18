from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.training.fedml.constants import UPDATE_QUEUED_EVENT
from src.protocol.training.fedml.model_update_meta import ModelUpdateMeta


class QueuedUpdate(Event):
    def __init__(self, update: ModelUpdateMeta, queue: [ModelUpdateMeta]):
        super().__init__(UPDATE_QUEUED_EVENT)
        self.update = update
        self.queue = queue


class UpdateQueue:

    def __init__(self, handler: Handler):
        self.handler = handler
        self.queued_updates = {}

    def queue(self, model_meta: ModelUpdateMeta):
        queue = self.get_queue(model_meta.round_id)
        queue.append(model_meta)
        self.handler.queue_event(QueuedUpdate(model_meta, queue))

    def get_queue(self, round_id: int) -> [ModelUpdateMeta]:
        if round_id not in self.queued_updates:
            self.queued_updates[round_id] = []
        return self.queued_updates.get(round_id)

    def get_unique_clusters(self, round_id: int) -> [str]:
        return set(map(lambda update: update.cluster_id,  self.get_queue(round_id)))