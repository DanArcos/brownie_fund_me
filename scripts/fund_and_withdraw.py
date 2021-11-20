from brownie import FundMe
from scripts.helpful_scripts import get_account


def fund():
    fund_me = FundMe[-1]  # Get the most recently depoyed fund me contract
    account = get_account()
    entrance_fee = (
        fund_me.getEntranceFee()
    )  # Get minimum ETH to meet 50 dollars, to 8 decimal places
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    fund_me.fund(
        {"from": account, "value": entrance_fee}
    )  # Send 50 dollars worth of ETH


def withdraw():
    print("Withdrawing....")
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})  # Withdraw everything


def main():
    fund()
    withdraw()
