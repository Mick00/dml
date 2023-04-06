import pytest

### Accounts ###
@pytest.fixture(scope="function")
def owner(accounts):
    return accounts[0]

@pytest.fixture(scope="function")
def deployer(accounts):
    return accounts[0]

@pytest.fixture(scope="function")
def trainer1(accounts):
    return accounts[1]

@pytest.fixture(scope="function")
def trainer2(accounts):
    return accounts[2]

@pytest.fixture(scope="function")
def receiver(accounts):
    return accounts[1]

### Contracts ###
@pytest.fixture(scope="function")
def trainers(owner, project):
    return owner.deploy(project.Trainer)

@pytest.fixture(scope="function")
def models(deployer, project):
    return deployer.deploy(project.Models)

@pytest.fixture(scope="function")
def updates(deployer, project, models):
    return deployer.deploy(project.Updates, models)