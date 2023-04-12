import ape
import pytest
from eth_abi import encode
from eth_hash.auto import keccak
from .utils import pad_ids, get_aggregate_hash

def test_append_generation(deployer, models):
    parent = models.root()
    assert models.modelExists(parent)
    child = b'100'
    ids = [2, 5]
    output = models.appendGeneration(parent, pad_ids(ids), "http://", sender=deployer)
    newGenHash = get_aggregate_hash(parent, ids)
    assert models.modelExists(b'10') == False
    assert models.modelExists(newGenHash)

def test_next_round(deployer, trainer1, trainer2, trainers, models):
    trainers.register(sender=trainer1)
    trainers.register(sender=trainer2)
    assert models.round() == 0
    models.nextRound(sender=trainer1)
    assert models.round() == 0
    models.nextRound(sender=trainer2)
    assert models.round() == 1
    models.nextRound(sender=trainer1)
    assert models.round() == 1
    models.nextRound(sender=trainer2)
    assert models.round() == 2