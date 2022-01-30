import logging
from os import getenv
from typing import Union

APP_LOG_LEVEL = getenv("APP_LOG_LEVEL", "INFO")


def get_logger(
    ctx: str = __name__,
    level: Union[int, str] = APP_LOG_LEVEL,
):
    print(f"Creating logger: ctx={ctx}, level={level}")
    logging.basicConfig(level=level)
    return logging.getLogger(ctx)
