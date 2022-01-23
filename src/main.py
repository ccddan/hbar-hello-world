from config import config
from utils import get_logger
from utils.hedera import Hedera, HederaAccount

logger = get_logger(__name__)

logger.info(f"Config: {config}")

root_account_id = Hedera.load_account_id()
root_private_key = Hedera.load_private_key()
client = Hedera.get_client(account_id=root_account_id, private_key=root_private_key)

account: HederaAccount = HederaAccount(client)
account.get_balance()
