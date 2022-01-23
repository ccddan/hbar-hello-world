from config import config
from utils import get_logger
from utils.hedera import Hedera, HederaAccount

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

# Create a new account
new_account: HederaAccount = HederaAccount(client)
logger.info(f"New account: {new_account}")


logger.info("\n\n")
logger.info("Tranfer from root account to new account")
txr = root_account.transfer(
    tinybars=100_000, account_id=new_account.account_id, memo="welcome"
)
logger.info(f"Transfer status: {root_account.tx_status(txr).toString()}")
logger.info(f"Transfer cost: {root_account.tx_receipt(txr).toString()}")

logger.info("\n\n")
logger.info(f"root account balance: {root_account.get_balance().hbars.toString()}")
logger.info(f"new account balance: {new_account.get_balance().hbars.toString()}")
