from brownie import TestToken, config, network
from scripts.helpful_scripts import get_account
import time


def main():
    test_token, account = deploy_contract()


def deploy_contract():
    account = get_account()
    # if len(TestToken) > 0:
    #     test_token = TestToken[-1]
    # else:
    #     test_token = TestToken.deploy(
    #         {"from": account},
    #         publish_source=config["networks"][network.show_active()].get(
    #             "verify", False
    #         ),
    #     )
    test_token = TestToken.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    return test_token, account
