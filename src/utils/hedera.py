from typing import Optional

from hedera import (
    AccountBalance,
    AccountBalanceQuery,
    AccountCreateTransaction,
    AccountId,
    Client,
    Hbar,
    PrivateKey,
    PublicKey,
    TransactionReceipt,
    TransactionResponse,
)

from config import DeploymentEnv, config
from utils import get_logger

logger = get_logger(__name__)


class Hedera:
    @staticmethod
    def load_account_id(id: Optional[str] = None) -> AccountId:
        return AccountId.fromString(id if id else config["account"]["id"])

    @staticmethod
    def load_private_key(private_key: Optional[str] = None) -> PrivateKey:
        return PrivateKey.fromString(
            private_key if private_key else config["account"]["private_key"]
        )

    @staticmethod
    def get_client(
        account_id: Optional[AccountId] = None, private_key: Optional[PrivateKey] = None
    ) -> Client:
        logger.debug(f"Hedera::get_client - create account_id")
        _account_id: AccountId = (
            account_id if account_id else Hedera.load_account_from_id()
        )

        logger.debug(f"Hedera::get_client - create account_id")
        private_key: PrivateKey = (
            private_key
            if private_key
            else Hedera.load_private_key(config["account"]["private_key"])
        )

        logger.debug(f"Hedera::get_client - create client")
        client: Client = (
            Client.forTestnet()
            if config["env"] == DeploymentEnv.Development.value
            else Client.forMainnet()
        )

        logger.debug(f"Hedera::get_client - set operator")
        client.setOperator(_account_id, private_key)

        logger.debug(f"Hedera::get_client - client: {client.toString()}")
        return client


class HederaAccount:
    def __init__(
        self,
        client,
        account_id: Optional[AccountId] = None,
        private_key: Optional[PrivateKey] = None,
    ) -> None:
        self.client: Client = client

        if account_id:
            logger.debug(
                f"HederaAccount::init - existent account id: {account_id.toString()}"
            )
            self.account_id = account_id
            self.private_key = private_key
            self.public_key = self.private_key.getPublicKey()
            self.tx_receipt: Optional[TransactionReceipt] = None

        else:
            self.private_key: PrivateKey = PrivateKey.generate()
            self.public_key: PublicKey = self.private_key.getPublicKey()

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
