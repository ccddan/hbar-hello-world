from time import sleep
from config import config
from utils import get_logger
from utils.hedera import HTS, Hedera, HederaAccount
from utils.token import TokenHandler

logger = get_logger(ctx=__name__)

logger.info(f"Config: {config}")

root_account_id = Hedera.load_account_id()
root_private_key = Hedera.load_private_key()
client = Hedera.get_client(
    account_id=root_account_id,
    private_key=root_private_key,
)

# Load root account
root_account: HederaAccount = HederaAccount(
    client=client,
    account_id=root_account_id,
    private_key=root_private_key,
)
logger.info(f"Root account: {root_account}")
logger.info("\n\n")

# Create a new account
new_account: HederaAccount = HederaAccount(client, initial_balance=900_000)
logger.info(f"New account: {new_account}")
logger.info("\n\n")

# Create token
token = HTS.create(
    client=client,
    account=root_account,
    name="ccddan",
    symbol="CCDD",
    initial_supply=10_000,
    decimals=2,
)

logger.info(f'Token ID: {token["tokenId"].toString()}')
logger.info(f'Token\'s node ID: {token["nodeId"].toString()}')
logger.info("\n\n")


logger.info(f"Root account info: {root_account.get_info().toString()}")
logger.info("\n\n")


# Create token handler
th: TokenHandler = TokenHandler(
    token_id=token["tokenId"],
    node_id=token["nodeId"],
    account=root_account,
    client=root_account.client,
)

logger.info("Associate user account to token")
rx = th.associate(new_account)
sleep(7)  # wait for association
logger.info(f"New account association with token: {rx.toString()}")
logger.info("\n")


logger.info("KYC on new account so it can receive tokens")
rx = th.kyc(new_account)
sleep(7)  # wait for KYC
logger.info(f"KYC result: {rx.toString()}")
logger.info("\n")


logger.info('Transfer "CCDD" tokens from treasury to new_account')
rx = th.transfer(
    amount=50,
    target_account=new_account,
)
sleep(7)  # wait for transfer to complete
logger.info(f'"CCDD" token transfer result: {rx.toString()}')
logger.info("\n\n\n")

logger.info(f"Root account info: {root_account.get_info().toString()}")
logger.info("\n")
logger.info(f"New account info: {new_account.get_info().toString()}")
