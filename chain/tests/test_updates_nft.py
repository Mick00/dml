import ape
import pytest
from .utils import pad_ids, get_aggregate_hash

def test_propose(deployer, trainer1, updates, models):
    parent = models.root()
    tx_deployer = updates.propose(parent, "ex uri", sender=deployer)
    tx_trainer = updates.propose(parent, "ex uri", sender=trainer1)
    assert updates.ownerOf(tx_deployer.events[0].updateId) == deployer
    assert updates.ownerOf(tx_trainer.events[0].updateId) == trainer1

def test_propose_init(updates, deployer, trainer1):
    parent = '0000000000000000000000000000000000000000000000000000000000000000'
    uri = 'C:\\\\Users\\\\micdu\\\\Code\\\\pythonProject\\\\dmtl\\\\lightning_data\\checkpoints\\1\\28757799ca1846a08f0e01eeb225519c\\checkpoints\\epoch=0-step=797.ckpt'
    tx_deployer = updates.propose(bytes.fromhex(parent), uri, sender=trainer1)

def test_propose_not_exists(updates, trainer1):
    parent = '0000000000000000000000000000000000000000000000000000000000000001'
    uri = 'C:\\\\Users\\\\micdu\\\\Code\\\\pythonProject\\\\dmtl\\\\lightning_data\\checkpoints\\1\\28757799ca1846a08f0e01eeb225519c\\checkpoints\\epoch=0-step=797.ckpt'
    with ape.reverts(expected_message="parent model does not exist"):
        tx_deployer = updates.propose(bytes.fromhex(parent), uri, sender=trainer1)

def test_aggregate(deployer, trainer1, updates, models):
    parent = models.root()
    prop_deployer = updates.propose(parent, "ex uri", sender=deployer)
    prop_trainer = updates.propose(parent, "ex uri", sender=trainer1)
    ids = [prop_deployer.events[0].updateId, prop_trainer.events[0].updateId]
    agg = updates.aggregate(pad_ids(ids), "aggregate", sender=deployer)
    assert agg.events[1].hash == get_aggregate_hash(parent, ids)
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