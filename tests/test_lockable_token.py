from brownie import TestToken, accounts, config, network, exceptions, convert
from web3 import Web3
from scripts.deploy import deploy_contract
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest
import eth_abi
import time


def test_can_mint():
    test_token, account = deploy_contract()
    mint_amount = 1000000
    tx = test_token.mint(mint_amount, {"from": account})
    assert test_token.totalSupply() == mint_amount
    assert test_token.balanceOf(account) == mint_amount


def test_can_lock():
    test_token, account = deploy_contract()
    account2 = get_account(name="DEV02")
    mint_amount = 1000000
    test_token.mint(mint_amount, {"from": account})
    test_token.lockToken(account2, {"from": account})
    assert test_token.addressTokenLocked(account) == True
    assert test_token.addressTokenController(account) == account2
    # non token holders cannot lock
    with pytest.raises(exceptions.VirtualMachineError):
        test_token.lockToken(account2, {"from": account2})
    # once locked transfer cannot be initiated from owner
    with pytest.raises(exceptions.VirtualMachineError):
        test_token.transfer(account2, mint_amount / 10, {"from": account})
    # once locked approved address cannot initiate transfer as well
    test_token.approve(account2, mint_amount / 10, {"from": account})
    with pytest.raises(exceptions.VirtualMachineError):
        test_token.transferFrom(account, account2, mint_amount / 10)


def test_can_unlock():
    test_token, account = deploy_contract()
    account2 = get_account(name="DEV02")
    mint_amount = 1000000
    test_token.mint(mint_amount, {"from": account})
    test_token.lockToken(account2, {"from": account})
    # once locked non controller cannot initiate unlock
    with pytest.raises(exceptions.VirtualMachineError):
        test_token.unlockToken(account, {"from": account})
    # controller can unlock token
    test_token.unlockToken(account, {"from": account2})
    assert test_token.addressTokenLocked(account) == False
    assert (
        test_token.addressTokenController(account)
        == "0x0000000000000000000000000000000000000000"
    )
    # once unlocked, token can be transferred
    test_token.transfer(account2, mint_amount / 10, {"from": account})
    assert test_token.balanceOf(account2) == mint_amount / 10
    assert test_token.balanceOf(account) == mint_amount - (mint_amount / 10)
