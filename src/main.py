from time import sleep
from config import config
from utils import get_logger
from hedera import TopicId
from utils.hedera import Hedera, HederaAccount
from utils.topic import TopicMessage, Topic, TopicSubscription

logger = get_logger(__name__)

logger.info(f"Config: {config}")

root_account_id = Hedera.load_account_id()
root_private_key = Hedera.load_private_key()
client = Hedera.get_client(account_id=root_account_id, private_key=root_private_key)

# Load root account
root_account: HederaAccount = HederaAccount(
    client, account_id=root_account_id, private_key=root_private_key
)
logger.info(f"Root account: {root_account}")
logger.info("\n\n")

# Create a new account
new_account: HederaAccount = HederaAccount(client)
logger.info(f"New account: {new_account}")
logger.info("\n\n")


logger.info("Tranfer HBAR from root account to new account")
tinybars_transfer_amount = 100_000
txr = root_account.transfer(
    tinybars=tinybars_transfer_amount, account_id=new_account.account_id, memo="welcome"
)
logger.info(f"Transfer status: {root_account.tx_status(txr).toString()}")
logger.info(f"Transfer cost: {root_account.tx_receipt(txr).toString()}")

logger.info("\n\n")
logger.info(f"root account balance: {root_account.get_balance().hbars.toString()}")
logger.info(f"new account balance: {new_account.get_balance().hbars.toString()}")
logger.info("\n\n")

topic_name = "Token Transfer"
logger.info(f"Create new topic: {topic_name}")
topic: Topic = Topic(client=client, memo=topic_name)
topic_id: TopicId = topic.get_id()
logger.info(f"Topic ID: {topic_id.toString()}")
logger.info("\t>Waiting for topic creation (consensus)...")
sleep(5)
logger.info("\n\n")

logger.info(f"Subscribe to topic")
sub1: TopicSubscription = TopicSubscription(client=client, topic_txr=topic.txr)
sub2: TopicSubscription = TopicSubscription(client=client, topic_txr=topic.txr)


logger.info(f"Publish message to topic: {topic_name}")
publisher: TopicMessage = TopicMessage(client=client, topic_id=topic_id)

publisher.emit(
    f"Account {new_account.account_id.toString()} received {tinybars_transfer_amount} tinybars"
)

logger.info("Waiting for subscribers to react to emitted message...")
sleep(10)
logger.info("Waiting time finished")
