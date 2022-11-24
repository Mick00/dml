import math

from src.daeclust.daecluste_helper import get_strategy
from src.daeclust.state.events import TrainerSelectedUpdates
from src.nsclust.nsclust_helpers import get_current_cluster
from src.daeclust.state.events import StartUpdateSelection
from src.protocol.client.actions.send import Send
from src.protocol.client.client_state_helpers import get_node_id
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.models.experiment import load_model
from src.protocol.training.models.operations import weight_divergence


class WDUpdateSelector(StateTransition):

    def transition(self, event: StartUpdateSelection, state: State, handler: Handler):
        my_id = get_node_id(state)
        current_cluster = get_current_cluster(state)
        update_pool = get_strategy(state)\
            .for_round(event.round_id)\
            .update_pools.for_cluster(current_cluster)
        my_update = list(filter(lambda update: update.from_id == my_id, update_pool))[0]
        my_update.divergence = 0
        my_update_model = load_model(my_update)
        selected = [my_update]
        for update in update_pool:
            if update.from_id != my_id:
                loaded_update = load_model(update)
                update.divergence = weight_divergence(my_update_model, loaded_update)
                selected.append(update)
        selected.sort(key=lambda update: update.divergence)
        if len(selected) <= 2:
            selected_top = selected
        else:
            selected_top = selected[0: math.floor(len(selected) * 0.90)]
        selected_trainers = list(map(lambda updates: updates.from_id, selected_top))
        selected_events = TrainerSelectedUpdates(event.round_id, my_id, current_cluster, selected_trainers)
        handler.queue_event(selected_events)
        handler.queue_event(Send(selected_events))




