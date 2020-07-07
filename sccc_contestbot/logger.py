import logging
import sys


def init_logger(mod_name):
    """
    모듈별 로거를 생성합니다.
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)-8s: [%(name)s] : %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
