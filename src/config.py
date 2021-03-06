from enum import Enum
from os import environ, getenv

from utils import get_logger, APP_LOG_LEVEL

logger = get_logger(ctx=__name__)


class DeploymentEnv(Enum):
    Development = "development"
    Production = "production"


DEPLOYMENT_ENV = getenv("DEPLOYMENT_ENV", DeploymentEnv.Development.value)
logger.debug(f"Deployment env: {DEPLOYMENT_ENV}")

if DEPLOYMENT_ENV == DeploymentEnv.Development.value:
    logger.info("Load .env file")
    from dotenv import load_dotenv

    load_dotenv()

__config = {
    "env": DEPLOYMENT_ENV,
    "log_level": APP_LOG_LEVEL,
    "network": environ["HEDERA_NETWORK"],
    "account": {
        "id": environ["OPERATOR_ID"],
        "private_key": environ["OPERATOR_KEY"],
    },
}


config = __config
