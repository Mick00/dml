from ape import project
from ape.cli import get_user_selected_account
import click
from ape.cli import network_option, NetworkBoundCommand, ape_cli_context
from ape.utils import ManagerAccessMixin
from ape.api.networks import LOCAL_NETWORK_NAME
from ape.logging import logger
import json
import os
from web3 import Web3

#perk you can add args unlike main method
@click.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
# cli_ctx must go first
def cli(cli_ctx, network):
    network = cli_ctx.provider.network.name
    if network == LOCAL_NETWORK_NAME or network.endswith("-fork"):
        account = cli_ctx.account_manager.test_accounts[0]
    else:
        account = get_user_selected_account()
    trainers = project.Trainers
    with open(os.path.join(ManagerAccessMixin.config_manager.PROJECT_FOLDER, 'address_book.json'), 'r') as f:
        addresses = json.load(f)
    trainers = trainers.at(addresses["trainers"]["address"])
    
    if not trainers.isRegistered(account):
        trainers.register(sender=account)
        logger.info("Registered")

    with open(os.path.join(ManagerAccessMixin.config_manager.PROJECT_FOLDER, '.build', "Trainers.json"), 'r') as f:
        abi = json.load(f)["abi"]
    provider = Web3(Web3.HTTPProvider("http://localhost:8545"))
    print(abi)
    print(json.load(addresses["trainers"]["abi"]))
    contract = provider.eth.contract(trainers.address, abi=abi)
    event_filter = contract.events["TrainerRegistered"].createFilter(fromBlock=0)
    for i in range(3):
        for event in event_filter.get_new_entries():
            print(event)