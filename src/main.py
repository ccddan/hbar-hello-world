from config import config
from utils import get_logger

logger = get_logger(__name__)

logger.info(f"Config: {config}")
