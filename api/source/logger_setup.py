import logging
import sys

import config


def init_logging():
    """Creating logger config"""
    logger = logging.getLogger("main")
    logger.setLevel(config.LOGLEVEL)
    logger.propagate = False
    fmt = logging.StreamHandler(stream=sys.stdout)
    fmt.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(filename)s:%(lineno)d: %(levelname)s] %(message)s'))

    fh = logging.FileHandler("api.log", mode='w', encoding='utf-8')
    logger.addHandler(fmt)
    logger.addHandler(fh)
