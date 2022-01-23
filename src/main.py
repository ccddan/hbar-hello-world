from utils.hedera import get_client


from config import DeploymentEnv, config
from utils import get_logger

logger = get_logger(__name__)

logger.info(f"Config: {config}")

client = get_client()
logger.info(f"hedera client: {client}")
