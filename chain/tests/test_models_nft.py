import ape
import pytest
from eth_abi import encode
from eth_hash.auto import keccak

def test_append_generation(deployer, models):
    parent = models.root()
    assert models.modelExists(parent)
    child = b'100'
    output = models.appendGeneration(parent, child, "http://", sender=deployer)
    newGenHash = keccak(encode(['bytes32', 'bytes32'], [parent, child]))
    assert models.modelExists(b'10') == False
    assert models.modelExists(newGenHash)

