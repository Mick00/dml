import ape
import pytest

def test_erc165(trainers):
    # ERC165 interface ID of ERC165
    assert trainers.supportsInterface("0x01ffc9a7")

    # ERC165 specifies that this is never supported
    assert not trainers.supportsInterface("0xffffffff")

    # ERC165 interface ID of ERC721
    assert trainers.supportsInterface("0x80ac58cd")

    # ERC165 interface ID of ERC721 Metadata Extension
    assert trainers.supportsInterface("0x5b5e139f")

    # ERC165 interface ID of ERC4494
    assert trainers.supportsInterface("0x5604e225")


def test_init(trainers, owner):
    assert trainers.balanceOf(owner) == 0
    with ape.reverts():
        assert trainers.ownerOf(0)


def test_register(trainers, accounts):
    assert trainers.balanceOf(accounts[0]) == 0
    assert trainers.balanceOf(accounts[1]) == 0
    trainers.register(sender=accounts[1])
    assert trainers.balanceOf(accounts[0]) == 0
    assert trainers.balanceOf(accounts[1]) == 1
    assert not trainers.isRegistered(accounts[0])
    assert trainers.isRegistered(accounts[1])
    assert trainers.ownerOf(1) == accounts[1]
    trainers.register(sender=accounts[0])
    assert trainers.balanceOf(accounts[0]) == 1
    assert trainers.balanceOf(accounts[1]) == 1
    assert trainers.isRegistered(accounts[0])
    assert trainers.isRegistered(accounts[1])
    assert trainers.ownerOf(2) == accounts[0]


def test_total_supply(trainers, accounts):
    assert trainers.totalSupply() == 0
    trainers.register(sender=accounts[0])
    assert trainers.totalSupply() == 1


def test_transfer(trainers, accounts):
    assert trainers.balanceOf(accounts[0]) == 0
    assert trainers.balanceOf(accounts[1]) == 0
    trainers.register(sender=accounts[0])
    assert trainers.balanceOf(accounts[0]) == 1
    assert trainers.ownerOf(1) == accounts[0].address
    trainers.transferFrom(accounts[0], accounts[1], 1, sender=accounts[0])
    assert trainers.balanceOf(accounts[0]) == 0
    assert trainers.balanceOf(accounts[1]) == 1
    assert trainers.ownerOf(1) == accounts[1].address
    trainers.transferFrom(accounts[1], accounts[0], 1, sender=accounts[1])
    assert trainers.balanceOf(accounts[1]) == 0
    assert trainers.balanceOf(accounts[0]) == 1
    assert trainers.ownerOf(1) == accounts[0].address


def test_incorrect_signer_transfer(trainers, owner, receiver):
    assert trainers.balanceOf(owner) == 0
    assert trainers.balanceOf(receiver) == 0
    trainers.register( sender=owner)
    with ape.reverts():
        trainers.transferFrom(owner,receiver,1,sender=receiver)    
    assert trainers.balanceOf(receiver) == 0
    assert trainers.balanceOf(owner) == 1
    assert trainers.ownerOf(1) == owner.address


def test_only_mint_one(trainers, owner):
    trainers.register(sender=owner)
    assert trainers.balanceOf(owner) == 1
    with ape.reverts():
        trainers.register(sender=owner)
    assert trainers.balanceOf(owner) == 1


def test_approve_transfer(trainers, owner, receiver):
    assert trainers.balanceOf(owner) == 0
    assert trainers.balanceOf(receiver) == 0
    trainers.register(sender=owner)
    assert trainers.balanceOf(receiver) == 0
    assert trainers.balanceOf(owner) == 1
    assert trainers.ownerOf(1) == owner.address
    
    with ape.reverts():
        trainers.approve(receiver, 1, sender=receiver)
        trainers.transferFrom(owner, receiver, 1, sender=receiver)
    assert trainers.balanceOf(receiver) == 0
    assert trainers.balanceOf(owner) == 1
    assert trainers.ownerOf(1) == owner.address

    trainers.approve(receiver, 1, sender=owner)
    assert trainers.getApproved(1) == receiver
    trainers.transferFrom(owner, receiver, 1, sender=receiver)
    assert trainers.balanceOf(receiver) == 1
    assert trainers.balanceOf(owner) == 0
    assert trainers.ownerOf(1) == receiver.address


def test_uri(trainers, owner):

    assert trainers.baseURI() == "ipfs://QmaZm1rAkt6kHTKTFX8GwEhtPMVMeAGJYMBvoAcJWTddwb"
    trainers.register(sender=owner)
    assert trainers.tokenURI(1) == "ipfs://QmaZm1rAkt6kHTKTFX8GwEhtPMVMeAGJYMBvoAcJWTddwb/1"

    trainers.setBaseURI("new base uri", sender=owner)
    assert trainers.baseURI() == "new base uri"
    assert trainers.tokenURI(1) == "new base uri/1"

