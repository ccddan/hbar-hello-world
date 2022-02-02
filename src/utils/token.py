from typing import Optional
from hedera import (
    AccountId,
    Client,
    TokenAssociateTransaction,
    TokenId,
    TransactionResponse,
    TokenGrantKycTransaction,
    TransferTransaction,
    TransactionReceipt,
)
from jnius import autoclass

Collections = autoclass("java.util.Collections")

from utils.hedera import HederaAccount


class TokenHandler:
    def __init__(
        self,
        token_id: TokenId,
        node_id: AccountId,
        account: HederaAccount,
        client: Client,
    ) -> None:
        self.token_id = token_id
        self.node_id = node_id
        self.account = account
        self.client = client

    def associate(self, account: HederaAccount) -> TransactionReceipt:
        tx: TokenAssociateTransaction = (
            TokenAssociateTransaction()
            .setNodeAccountIds(Collections.singletonList(account.node_id))
            .setAccountId(account.account_id)
            .setTokenIds(Collections.singletonList(self.token_id))
            .freezeWith(self.client)
            .sign(self.account.private_key)
            .sign(account.private_key)
        )

        txr: TransactionResponse = tx.execute(self.client)

        return txr.getReceipt(self.client)

    def kyc(self, account: HederaAccount) -> TransactionReceipt:
        tx: TokenGrantKycTransaction = (
            TokenGrantKycTransaction()
            .setNodeAccountIds(Collections.singletonList(self.node_id))
            .setAccountId(account.account_id)
            .setTokenId(self.token_id)
        )

        txr: TransactionResponse = tx.execute(self.client)

        return txr.getReceipt(self.client)

    def transfer(
        self,
        amount: int,
        target_account: HederaAccount,
        source_account: Optional[HederaAccount] = None,
    ) -> TransactionReceipt:
        if source_account:
            # Transfer from one account to another
            tx: TransferTransaction = (
                TransferTransaction()
                .setNodeAccountIds(Collections.singletonList(self.node_id))
                .addTokenTransfer(
                    self.token_id,
                    source_account.account_id,
                    -amount,
                )
                .addTokenTransfer(
                    self.token_id,
                    target_account.account_id,
                    amount,
                )
                .freezeWith(self.client)
                .sign(source_account.private_key)
            )
        else:
            # Transfer from treasury
            tx: TransferTransaction = (
                TransferTransaction()
                .setNodeAccountIds(Collections.singletonList(self.node_id))
                .addTokenTransfer(
                    self.token_id,
                    self.account.account_id,
                    -amount,
                )
                .addTokenTransfer(
                    self.token_id,
                    target_account.account_id,
                    amount,
                )
            )

        txr: TransactionResponse = tx.execute(self.client)

        return txr.getReceipt(self.client)
