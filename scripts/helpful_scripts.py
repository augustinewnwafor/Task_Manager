from brownie import accounts, network, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "hardhat", "mainnet-fork"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]


def get_account(index=None, id=None):
    """
    Get an account to use for deployment or interaction.
    - If on local dev chain: use brownie accounts[0] or accounts.add with private key
    - If on testnet/mainnet: load from config
    """
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]

    # Otherwise, use private key from brownie-config.yaml
    return accounts.add(config["wallets"]["from_key"])
