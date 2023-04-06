from eth_abi import encode
from eth_hash.auto import keccak

def pad_ids(ids):
    return [ids[i] if i < len(ids) else 0 for i in range(50)]

def get_gen_hash(parent, child):
    return keccak(encode(['bytes32', 'bytes32'], [parent, child]))

def get_child_hash(updates):
    return keccak(encode(["uint256"]*50, pad_ids(updates)))

def get_aggregate_hash(parent, updates):
    return get_gen_hash(parent, get_child_hash(updates))