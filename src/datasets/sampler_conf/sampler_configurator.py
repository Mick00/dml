from src.datasets.data_helpers import apply_balance_rule, apply_partitions_rule, data_n_partitions, \
    data_partition_index, apply_target_bounds, get_higher_bound, get_lower_bound, apply_normal_probability, \
    get_distribution_std, get_distribution_mean
from src.datasets.data_loader import get_data_loader
from src.datasets.sampling_rules.balance import balanced_weight
from src.datasets.sampling_rules.normal import normal_probability_weights
from src.datasets.sampling_rules.partition import partition_subset
from src.datasets.sampling_rules.target import target_subset
from src.protocol.states.event import Event
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition, Handler


class ConfigureSampler(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        data_loader = get_data_loader(state)
        rules = []
        if apply_balance_rule(state):
            rules.append(balanced_weight())
        if apply_partitions_rule(state):
            rules.append(partition_subset(data_partition_index(state), data_n_partitions(state)))

        if apply_target_bounds(state):
            rules.append(target_subset(get_lower_bound(state), get_higher_bound(state)))
        elif apply_normal_probability(state):
            rules.append(normal_probability_weights(get_distribution_mean(state), get_distribution_std(state)))
        data_loader.set_sampling_rules(rules)