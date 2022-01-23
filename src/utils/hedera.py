from hedera import AccountId, Client, PrivateKey

from config import DeploymentEnv, config
from utils import get_logger

logger = get_logger(__name__)


def get_client():
    logger.debug(f"get_client - create account_id")
    account_id = AccountId.fromString(config["account"]["id"])

    logger.debug(f"get_client - create account_id")
    private_key = PrivateKey.fromString(config["account"]["private_key"])

    logger.debug(f"get_client - create client")
    client = (
        Client.forTestnet()
        if config["env"] == DeploymentEnv.Development.value
        else Client.forMainnet()
    )

    logger.debug(f"get_client - set operator")
    client.setOperator(account_id, private_key)

    return client
