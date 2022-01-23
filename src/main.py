from config import config
from utils import get_logger
from utils.hedera import Hedera, HederaAccount

logger = get_logger(__name__)

logger.info(f"Config: {config}")

client = Hedera.get_client()

account: HederaAccount = HederaAccount(client)
account.get_balance()
