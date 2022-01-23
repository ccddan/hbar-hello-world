from hedera import (
    Hbar,
    AccountCreateTransaction,
    AccountId,
    Client,
    PrivateKey,
    PublicKey,
    AccountBalance,
    AccountBalanceQuery,
    TransactionResponse,
    TransactionReceipt,
)

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


class HederaAccount:
    def __init__(self, client) -> None:
        self.private_key: PrivateKey = PrivateKey.generate()
        self.public_key: PublicKey = self.private_key.getPublicKey()
        self.client: Client = client

        tx_resp: TransactionResponse = (
            AccountCreateTransaction()
            .setKey(self.public_key)
            .setInitialBalance(Hbar.fromTinybars(1000))
            .execute(client)
        )

        self.tx_receipt: TransactionReceipt = tx_resp.getReceipt(self.client)
        self.account_id: AccountId = self.tx_receipt.accountId
        logger.debug(
            f"HederaAccount::init - new account id: {self.account_id.toString()}"
        )

    def get_balance(self):
        balance: AccountBalance = (
            AccountBalanceQuery().setAccountId(self.account_id).execute(self.client)
        )
        logger.debug(
            f"HederaAccount::get_balance - balance: {balance.hbars.toString()}"
        )
