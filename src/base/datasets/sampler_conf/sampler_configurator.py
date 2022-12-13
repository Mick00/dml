from src.base.datasets.data_helpers import apply_balance_rule, apply_partitions_rule, data_n_partitions, \
    data_partition_index, apply_target_bounds, get_higher_bound, get_lower_bound, apply_normal_probability, \
    get_distribution_std, get_distribution_mean, get_n_samples
from src.base.datasets.data_loader import get_data_loader
from src.base.datasets.sampling_rules.balance import balanced_weight
from src.base.datasets.sampling_rules.normal import normal_probability_weights
from src.base.datasets.sampling_rules.partition import partition_subset
from src.base.datasets.sampling_rules.target import target_subset
from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.event_handler import EventHandler, Handler


class ConfigureSampler(EventHandler):
    def _transition(self, event: Event, state: State, handler: Handler):
        data_loader = get_data_loader(state)
        rules = []
        log_dict = {}
        if apply_balance_rule(state):
            rules.append(balanced_weight())
            log_dict["balanced"] = True
        if apply_partitions_rule(state):
            index = data_partition_index(state)
            n_partitions =data_n_partitions(state)
            rules.append(partition_subset(index, n_partitions))
            log_dict = log_dict | {"partition_index": index, "n_partitions": n_partitions}

        if apply_target_bounds(state):
            lower_bound = get_lower_bound(state)
            higher_bound = get_higher_bound(state)
            rules.append(target_subset(lower_bound, higher_bound))
            log_dict = log_dict | {"lower_bound": lower_bound, "higher_bound": higher_bound }
        if apply_normal_probability(state):
            mean = get_distribution_mean(state)
            std = get_distribution_std(state)
            rules.append(normal_probability_weights(mean, std))
            log_dict = log_dict | {"mean": mean, "std": std}
        data_loader.set_sampling_rules(rules)
        n_samples = get_n_samples(state)
        log_dict["n_samples"] = n_samples
        data_loader.set_n_samples(n_samples)
        data_loader.set_sampler_tags(log_dict)
        return [self.log_info("sampler.config", log_dict)]