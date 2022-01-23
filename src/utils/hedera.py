from hedera import AccountId, Client, PrivateKey

from config import DeploymentEnv, config
from utils import get_logger

logger = get_logger(__name__)


class Hedera:
    @staticmethod
    def get_client() -> Client:
        logger.debug(f"Hedera::get_client - create account_id")
        account_id: AccountId = AccountId.fromString(config["account"]["id"])

        logger.debug(f"Hedera::get_client - create account_id")
        private_key: PrivateKey = PrivateKey.fromString(
            config["account"]["private_key"]
        )

        logger.debug(f"Hedera::get_client - create client")
        client: Client = (
        Client.forTestnet()
        if config["env"] == DeploymentEnv.Development.value
        else Client.forMainnet()
    )

        logger.debug(f"Hedera::get_client - set operator")
    client.setOperator(account_id, private_key)

        logger.debug(f"Hedera::get_client - client: {client.toString()}")
    return client
