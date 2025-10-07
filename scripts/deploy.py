import os
from dotenv import load_dotenv
load_dotenv()
from brownie import TodoList, network, config
from scripts.helpful_scripts import get_account


def deploy_todo_list():
    account = get_account()
    print(f"Deploying TodoList from {account} on {network.show_active()}")

    # publish_source=True triggers Etherscan verification
    todo = TodoList.deploy({"from": account}, publish_source=config["networks"][network.show_active()].get("verify", False))

    print(f"Contract deployed at {todo.address}")
    return todo


def main():
    deploy_todo_list()
