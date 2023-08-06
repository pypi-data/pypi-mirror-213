import logging

# _________________________________________________________________ #
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s | %(levelname)s | %(lineno)d] %(message)s',
                    datefmt='%H:%M:%S')


# _________________________________________________________________ #
def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger

# _________________________________________________________________ #

