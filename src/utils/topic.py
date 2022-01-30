from typing import Optional

from hedera import (
    Client,
    TopicId,
    PyConsumer,
    TopicCreateTransaction,
    TopicMessageQuery,
    TopicMessageSubmitTransaction,
    TransactionResponse,
    TopicId,
)

from utils import get_logger

logger = get_logger(ctx=__name__)


class Topic:
    def __init__(self, client: Client, memo: Optional[str] = "N/A") -> None:
        self.client = client
        self.topic: TopicCreateTransaction = TopicCreateTransaction().setTopicMemo(memo)
        self.txr: TransactionResponse = self.topic.execute(self.client)

    def get_id(self) -> TopicId:
        return self.txr.getReceipt(self.client).topicId


class TopicSubscription:
    def __init__(self, client: Client, topic_txr: TransactionResponse) -> None:
        self.client = client
        self.topic_txr = topic_txr
        self.topic_id = self.topic_txr.getReceipt(self.client).topicId

        self.subscription: TopicMessageQuery = (
            TopicMessageQuery()
            .setTopicId(self.topic_id)
            .subscribe(
                self.client,
                PyConsumer(
                    lambda timestamp, argc, *argv: logger.info(
                        f"subscription result:\n\tTimestamp: {timestamp}\n\tPayload size: {argc}\n\tPayload: {argv}"
                    )
                ),
            )
        )


class TopicMessage:
    def __init__(self, client: Client, topic_id: TopicId) -> None:
        self.client = client
        self.topic_id = topic_id

    def emit(self, msg: str) -> TransactionResponse:

        txr: TransactionResponse = (
            TopicMessageSubmitTransaction()
            .setTopicId(self.topic_id)
            .setMessage(msg)
            .execute(self.client)
        )

        return txr
