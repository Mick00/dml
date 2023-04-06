import ape
import pytest
from .utils import pad_ids, get_aggregate_hash

def test_propose(deployer, trainer1, updates, models):
    parent = models.root()
    tx_deployer = updates.propose(parent, "ex uri", sender=deployer)
    tx_trainer = updates.propose(parent, "ex uri", sender=trainer1)
    assert updates.ownerOf(tx_deployer.events[0].updateId) == deployer
    assert updates.ownerOf(tx_trainer.events[0].updateId) == trainer1

def test_aggregate(deployer, trainer1, updates, models):
    parent = models.root()
    prop_deployer = updates.propose(parent, "ex uri", sender=deployer)
    prop_trainer = updates.propose(parent, "ex uri", sender=trainer1)
    ids = [prop_deployer.events[0].updateId, prop_trainer.events[0].updateId]
    agg = updates.aggregate(pad_ids(ids), "aggregate", sender=deployer)
    assert agg.events[0].hash == get_aggregate_hash(parent, ids)
    assert models.modelExists(get_aggregate_hash(parent, ids))

def test_aggregate_unordered(deployer, trainer1, updates, models):
    parent = models.root()
    prop_deployer = updates.propose(parent, "ex uri", sender=deployer)
    prop_trainer = updates.propose(parent, "ex uri", sender=trainer1)
    ids = [prop_trainer.events[0].updateId, prop_deployer.events[0].updateId]
    with ape.reverts():
        updates.aggregate(pad_ids(ids), "aggregate", sender=deployer)

def test_aggregate_wrong_parent(deployer, trainer1, updates, models):    
    parent = models.root()
    prop_deployer = updates.propose(parent, "ex uri", sender=deployer)
    prop_trainer = updates.propose(parent, "ex uri", sender=trainer1)
    ids = [prop_deployer.events[0].updateId, prop_trainer.events[0].updateId]
    agg = updates.aggregate(pad_ids(ids), "aggregate", sender=deployer)
    new_parent = get_aggregate_hash(parent, ids)
    prop_deployer = updates.propose(parent, "ex uri", sender=deployer)
    prop_trainer = updates.propose(new_parent, "ex uri", sender=trainer1)
    ids = [prop_deployer.events[0].updateId, prop_trainer.events[0].updateId]
    with ape.reverts():
        updates.aggregate(pad_ids(ids), "aggregate", sender=deployer)