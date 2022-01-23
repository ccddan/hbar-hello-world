import logging


def get_logger(
    ctx: str = __name__,
    level: int = logging.DEBUG,
):
    print(f"Creating logger: ctx={ctx}, level={level}")
    logging.basicConfig(level=level)
    return logging.getLogger(ctx)
