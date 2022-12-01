from src.daeclust.daecluste_helper import get_strategy
from src.daeclust.state.events import UpdatePooled
from src.base.client.client_state_helpers import get_node_id
from src.base.client.messages.message import Message
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.fedml.model_update_meta import ModelUpdateMeta


class UpdateHandler(StateTransition):
    def transition(self, event: Message, state: State, handler: Handler):
        from_id = event.from_id if hasattr(event, "from_id") else get_node_id(state)
        update_meta = ModelUpdateMeta(
            event.data.cluster_id,
            event.data.round_id,
            event.data.model_name,
            event.data.checkpoint_uri,
            from_id
        )
        strat = get_strategy(state)
        round_strat = strat.for_round(event.data.round_id)
        round_strat.update_pools.add_update(update_meta)
        handler.queue_event(UpdatePooled(update_meta))