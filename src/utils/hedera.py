from enum import Enum
from typing import Optional

from hedera import (
    AccountBalance,
    AccountBalanceQuery,
    AccountCreateTransaction,
    AccountId,
    AccountInfo,
    AccountInfoQuery,
    Client,
    Hbar,
    PrivateKey,
    PublicKey,
    TokenCreateTransaction,
    TokenSupplyType,
    TokenType,
    TransactionReceipt,
    TransactionResponse,
    TransferTransaction,
)
from jnius import autoclass

from config import DeploymentEnv, config
from utils import get_logger

Collections = autoclass("java.util.Collections")

logger = get_logger(ctx=__name__)


class HbarDenominations(Enum):
    GIGABAR = 1_000_000_000
    MEGABAR = 1_000_000
    KILOBAR = 1_000
    HBAR = 1
    MILLIBAR = 1_000
    MICROBAR = 1_000_000
    TINYBAR = 100_000_000


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
        account_id: Optional[AccountId] = None,
        private_key: Optional[PrivateKey] = None,
    ) -> Client:
        logger.debug("Hedera::get_client - create account_id")

        if account_id:
            _account_id: AccountId = account_id
        else:
            _account_id: AccountId = Hedera.load_account_id()

        logger.debug("Hedera::get_client - create account_id")
        private_key: PrivateKey = (
            private_key
            if private_key
            else Hedera.load_private_key(config["account"]["private_key"])
        )

        logger.debug("Hedera::get_client - create client")
        client: Client = (
            Client.forTestnet()
            if config["env"] == DeploymentEnv.Development.value
            else Client.forMainnet()
        )

        logger.debug("Hedera::get_client - set operator")
        client.setOperator(_account_id, private_key)

        # IMPORTANT: let client to determine tx fee
        # client.setMaxTransactionFee(Hbar(HbarDenominations.HBAR.value * 10))

        logger.debug(f"Hedera::get_client - client: {client.toString()}")
        return client


class HederaAccount:
    def __init__(
        self,
        client,
        account_id: Optional[AccountId] = None,
        private_key: Optional[PrivateKey] = None,
        initial_balance: Optional[int] = 1_000_000,
    ) -> None:
        self.client: Client = client

        if account_id:
            logger.debug(
                f"""HederaAccount::init - existent account id: \
                {account_id.toString()}"""
            )

            if not private_key:
                raise Exception(
                    """When loading an existing account, \
                    'private_key' is required"""
                )

            self.account_id = account_id
            self.private_key = private_key
            self.public_key = self.private_key.getPublicKey()
            self.node_id = None

        else:
            self.private_key: PrivateKey = PrivateKey.generate()
            self.public_key: PublicKey = self.private_key.getPublicKey()

            txr: TransactionResponse = (
                AccountCreateTransaction()
                .setKey(self.public_key)
                .setInitialBalance(Hbar.fromTinybars(initial_balance))
                .execute(client)
            )
            self.node_id: AccountId = txr.nodeId

            tx_receipt: TransactionReceipt = txr.getReceipt(self.client)
            self.account_id: AccountId = tx_receipt.accountId
            logger.debug(
                f"""HederaAccount::init - new account id: \
                {self.account_id.toString()}"""
            )

    def get_balance(self):
        balance: AccountBalance = (
            AccountBalanceQuery()
            .setAccountId(
                self.account_id,
            )
            .execute(self.client)
        )
        logger.debug(
            f"""HederaAccount::get_balance - balance: \
            {balance.hbars.toString()}"""
        )

        return balance

    def transfer(
        self, tinybars: int, account_id: AccountId, memo: Optional[str] = None
    ) -> TransactionResponse:
        logger.debug(
            f"""HederaAccount::transfer - from={self.account_id.toString()}, \
            to={account_id.toString()}"""
        )
        logger.debug(f"HederaAccount::transfers - tinybars: {tinybars}")
        logger.debug(f"HederaAccount::transfers - memo: {memo}")

        amount: Hbar = Hbar.fromTinybars(tinybars)
        tx: TransferTransaction = (
            TransferTransaction()
            .addHbarTransfer(self.account_id, amount.negated())
            .addHbarTransfer(account_id, amount)
        )

        if memo:
            tx.setTransactionMemo(memo)

        txr: TransactionResponse = tx.execute(self.client)

        return txr

    def tx_status(self, txr: TransactionResponse):
        return txr.getReceipt(self.client).status

    def tx_receipt(self, txr: TransactionResponse):
        return txr.getReceipt(self.client)

    def get_info(self) -> AccountInfo:
        return (
            AccountInfoQuery()
            .setAccountId(
                self.account_id,
            )
            .execute(self.client)
        )

    # Overridden methods
    def __iter__(self):
        yield "account_id", self.account_id.toString()
        yield "private_key", f"""{self.private_key.toString()[:5]}...{self.private_key.toString()[-5:]}"""
        yield "public_key", f"""{self.public_key.toString()[:5]}...{self.public_key.toString()[-5:]}"""
        yield "balance", self.get_balance().hbars.toString()
        yield "node_id", f"""{self.node_id.toString() if self.node_id else self.node_id}"""

    def __str__(self) -> str:
        return f"{dict(self)}"


class HTS:
    @staticmethod
    def create(
        client: Client,
        account: HederaAccount,
        name: str,
        symbol: str,
        decimals: int = 0,
        initial_supply: int = 0,
        max_supply: int = 1_000_000_000,
    ):
        tx: TokenCreateTransaction = (
            TokenCreateTransaction()
            .setTokenName(name)
            .setTokenSymbol(symbol)
            .setTokenType(TokenType.FUNGIBLE_COMMON)
            .setSupplyType(TokenSupplyType.FINITE)
            .setDecimals(decimals)
            .setInitialSupply(initial_supply)
            .setMaxSupply(max_supply)
            .setTreasuryAccountId(account.account_id)
            .setAdminKey(account.public_key)
            .setFreezeKey(account.public_key)
            .setWipeKey(account.public_key)
            .setKycKey(account.public_key)
            .setSupplyKey(account.public_key)
            .setFreezeDefault(False)
            .freezeWith(client)
        )

        if account.node_id:
            tx.setNodeAccountIds(Collections.singletonList(account.node_id))

        # tx.freezeWith(client)
        tx.sign(account.private_key)

        txr: TransactionResponse = tx.execute(client)

        return {
            "tokenId": txr.getReceipt(client).tokenId,
            "nodeId": txr.nodeId,
        }
