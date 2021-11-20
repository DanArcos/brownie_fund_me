from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    print("Begin Deployment")

    account = get_account()

    # Pass price feed to fundMe Contract

    # if on a persistent network, use the associated addres, otehrwise deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    # Use fake aggregator when deploying
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        print("Mocks deployed")

    # Deploy fund me contract
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )  # Since there's a state change to the blockchain, must always use from account
    print(f"contract deployed to {fund_me.address}")

    # Return fund_me contract object, for testing use
    return fund_me


def main():
    deploy_fund_me()
