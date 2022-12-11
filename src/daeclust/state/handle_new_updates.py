from src.daeclust.daecluste_helper import get_strategy
from src.daeclust.state.events import UpdatesPooled
from src.base.client.client_state_helpers import get_node_id
from src.base.client.messages.message import Message
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple
from src.base.training.fedml.model_update_meta import ModelUpdateMeta


class UpdateHandler(EventHandlerSimple):
    def transition(self, event: Message, state: State, handler: EventListener):
        from_id = event.from_id if hasattr(event, "from_id") else get_node_id(state)
        updates = event.data.updates
        round_id = updates[0].get("round_id")
        strat = get_strategy(state)
        for update in updates:
            update_meta = ModelUpdateMeta(
                update.get("cluster_id"),
                update.get("round_id"),
                update.get("model_name"),
                update.get("checkpoint_uri"),
                from_id
            )
            strat.add_update(update_meta)
        round_strategy = strat.for_round(round_id)
        len_trainers_udpates = len(round_strategy.update_pools.trainers_entered)
        handler.queue_event(UpdatesPooled(round_id, len_trainers_udpates))