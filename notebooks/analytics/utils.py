

def get_runs(client, exp, n_rounds):
    runs = client.search_runs(experiment_ids=exp.experiment_id, filter_string="tags.round_id='0'")
    for i in range(1, n_rounds):
        i_runs = client.search_runs(experiment_ids=exp.experiment_id, filter_string=f"tags.round_id='{i}'")
        runs = runs + i_runs
    return runs