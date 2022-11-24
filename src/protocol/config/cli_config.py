import argparse


def get_arg_parse():
    parser = argparse.ArgumentParser(description='Launch a decentralised ML node')
    parser.add_argument('--data_path')
    parser.add_argument('--broker_hostname')
    parser.add_argument('--broker_port', type=int, default=5672)
    parser.add_argument('--trainer_threshold', type=int)
    parser.add_argument('--local_model')
    parser.add_argument('--training_out')
    parser.add_argument('--tracking_uri', default="http://localhost:5000")
    parser.add_argument('--experiment_name', default="declust")
    return parser