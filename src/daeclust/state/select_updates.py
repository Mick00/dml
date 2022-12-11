import numpy as np

from src.daeclust.daecluste_helper import get_strategy, get_div_tolerance
from src.daeclust.state.events import TrainerSelectedUpdates
from src.nsclust.nsclust_helpers import get_current_cluster
from src.daeclust.state.events import StartUpdateSelection
from src.base.client.actions.send import Send
from src.base.client.client_state_helpers import get_node_id
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.base.training.models.experiment import load_model
from src.base.training.models.operations import weight_divergence


class WDUpdateSelector(EventHandler):

    def _transition(self, event: StartUpdateSelection, state: State, handler: EventListener):
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
                update.divergence = weight_divergence(my_update_model, loaded_update).item()
                selected.append(update)
        selected.sort(key=lambda update: update.divergence)
        all_divergences = list(map(lambda exp: exp.divergence, selected))
        log_all_wd = self.log_info("cluster_aggregation.weight_divergences", {
            "round_id": event.round_id,
            "sum": all_divergences,
            "trainers": list(map(lambda exp: exp.from_id, selected))
        })
        if len(selected) <= 2:
            selected_top = selected
        else:
            std_dev = np.array(all_divergences).std()
            div_tolerance = std_dev * get_div_tolerance(state)
            selected_top = filter(lambda update: update.divergence <= div_tolerance, selected)
        selected_trainers = list(map(lambda updates: updates.from_id, selected_top))
        selected_events = TrainerSelectedUpdates(event.round_id, my_id, current_cluster, selected_trainers)
        handler.queue_event(selected_events)
        handler.queue_event(Send(selected_events))
        return [
            log_all_wd,
            self.log_info("cluster_aggregation.weight_divergences.selected", {
                "round_id": event.round_id,
                "selected_trainers": selected_trainers,
                "sum": list(map(lambda exp: exp.divergence, selected))
            })
        ]




