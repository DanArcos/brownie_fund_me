from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()

    # Deploy new fund me contract
    fund_me = deploy_fund_me()

    # Get the entrace fee
    entrance_fee = fund_me.getEntranceFee() + 100

    # Get the first transaction, the funding amount
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)

    # Test
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()  # Add random account

    # Look to see if withdrawing from another account raises a different exception
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})  # Should pass
