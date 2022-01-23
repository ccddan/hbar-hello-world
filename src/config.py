from os import environ, getenv
from utils import get_logger

logger = get_logger(__name__)

DEPLOYMENT_ENV = getenv("DEPLOYMENT_ENV", "production")
logger.debug(f"Deployment env: {DEPLOYMENT_ENV}")

if DEPLOYMENT_ENV == "development":
    logger.info(f"Load .env file")
    from dotenv import load_dotenv

    load_dotenv()

__config = {
    "env": DEPLOYMENT_ENV,
    "network": environ["HEDERA_NETWORK"],
    "account": {
        "id": environ["OPERATOR_ID"],
        "private_key": environ["OPERATOR_KEY"],
    },
}


config = __config
