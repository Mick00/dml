from src.base.client.actions.send import Send
from src.base.states.event_handler import EventHandlerSimple
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.training.events import ModelTrained
from src.base.training.fedml.events import ClusterUpdate


class ShareUpdate(EventHandlerSimple):
    def transition(self, event: ModelTrained, state: State, handler: EventListener):
        handler.queue_event(Send(ClusterUpdate(event.exp)))
