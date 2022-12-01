from src.nsclust.nsclust_helpers import get_model_loader
from src.nsclust.events import SelectedUpdates, AggregationCompleted
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple


class Aggregate(EventHandlerSimple):
    def transition(self, event: SelectedUpdates, state: State, handler: EventListener):
        update_queue = event.selected_updates
        model_loader = get_model_loader(state)
        for update in update_queue:
            if model_loader.cluster_exists(update.cluster_id):
                model_loader\
                    .get_cluster(update.cluster_id)\
                    .get_round(update.round_id)\
                    .add_update(update.checkpoint_uri)
            else:
                model_loader.set_cluster_genesis(update.cluster_id, update.model_name, update.checkpoint_uri, round_id=update.round_id)
        handler.queue_event(AggregationCompleted(event.round_id))
