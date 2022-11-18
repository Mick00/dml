from src.protocol.client.actions.send import Send
from src.protocol.client.client_state_helpers import get_node_id
from src.protocol.client.messages.message import Message
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.fedml.events import ClusterUpdate
from src.protocol.training.fedml.fedml_state_helper import get_update_queue
from src.protocol.training.fedml.model_update_meta import ModelUpdateMeta
from src.protocol.training.train_model import ModelTrained


class ShareUpdate(StateTransition):
    def transition(self, event: ModelTrained, state: State, handler: Handler):
        event = ClusterUpdate(event.model)
        handler.queue_event(event)
        handler.queue_event(Send(event))


class ReceiveUpdate(StateTransition):
    def transition(self, event: Message, state: State, handler: Handler):
        from_id = event.from_id if hasattr(event, "from_id") else get_node_id(state)
        update_meta = ModelUpdateMeta(
            event.data.cluster_id,
            event.data.round_id,
            event.data.model_name,
            event.data.checkpoint_uri,
            from_id
        )
        get_update_queue(state).queue(update_meta)
