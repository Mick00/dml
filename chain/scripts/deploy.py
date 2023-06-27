from ape import project
from ape.cli import get_user_selected_account
import click
from ape.cli import network_option, NetworkBoundCommand, ape_cli_context
from ape.utils import ManagerAccessMixin
from ape.api.networks import LOCAL_NETWORK_NAME
from ape.logging import logger
import json
import os

# default connect to a provider
def main():
    account = get_user_selected_account()
    registry = account.deploy(project.Registry)
    logger.info(registry.address)
    addressbook.set_global_entry("registry", registry.address)

def get_abi(contract_name):
    with open(os.path.join(ManagerAccessMixin.config_manager.PROJECT_FOLDER, '.build', '{}.json'.format(contract_name)), 'r') as f:
        return json.load(f)["abi"]

def get_address_book_entry(contract_container):
    abi = [fn.json() for fn in contract_container.contract_type.abi]
    return {
        contract_container.contract_type.name.lower(): {
            "abi": abi,
            "address": contract_container.deployments[-1].address
        }
    }

#perk you can add args unlike main method
@click.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
# cli_ctx must go first
def cli(cli_ctx, network):
    """
    Deploy the contracts
    """
    network = cli_ctx.provider.network.name
    if network == LOCAL_NETWORK_NAME or network.endswith("-fork"):
        account = cli_ctx.account_manager.test_accounts[0]
    else:
        account = get_user_selected_account()


    registry = account.deploy(project.Registry)
    trainers = account.deploy(project.Trainers)
    models = account.deploy(project.Models, trainers.address)
    updates = account.deploy(project.Updates, models.address)

    addresses = get_address_book_entry(project.Registry) | \
        get_address_book_entry(project.Trainers) | \
        get_address_book_entry(project.Models) | \
        get_address_book_entry(project.Updates)

    with open(os.path.join(ManagerAccessMixin.config_manager.PROJECT_FOLDER,"export" ,'address_book.json'), 'w') as f:
        json.dump(addresses, f, ensure_ascii=False)
