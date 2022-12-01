from src.base.client.actions.send import Send
from src.base.client.client_state_helpers import get_node_id
from src.base.client.messages.message import Message
from src.base.logging.logging_helpers import get_logger
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.base.training.fedml.events import ClusterUpdate
from src.base.training.fedml.fedml_state_helper import get_update_queue
from src.base.training.fedml.model_update_meta import ModelUpdateMeta
from src.base.training.train_model import ModelTrained


class ShareUpdate(EventHandler):
    def transition(self, event: ModelTrained, state: State, handler: EventListener):
        event = ClusterUpdate(event.exp)
        handler.queue_event(event)
        handler.queue_event(Send(event))


class ReceiveUpdate(EventHandler):
    def transition(self, event: Message, state: State, handler: EventListener):
        from_id = event.from_id if hasattr(event, "from_id") else get_node_id(state)
        update_meta = ModelUpdateMeta(
            event.data.cluster_id,
            event.data.round_id,
            event.data.model_name,
            event.data.checkpoint_uri,
            from_id
        )
        get_logger(state).info(event.type, extra={
            "round_id": update_meta.round_id,
            "from_id": update_meta.from_id,
            "cluster_id": update_meta.cluster_id,
            "checkpoint_uri": update_meta.checkpoint_uri,
            "model_name": update_meta.model_name
        })
        get_update_queue(state).queue(update_meta)
