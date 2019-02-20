# -*- coding: utf-8 -*-
__author__ = 'nmaekawa'
__email__ = 'nmaekawa@g.harvard.edu'
__version__ = '0.1.0'


# logging setup borrowed from urllib3
# https://github.com/urllib3/urllib3
import logging
from logging import NullHandler


# set default logging handler to avoid "no handler found" warning
logging.getLogger(__name__).addHandler(NullHandler)

def add_stderr_logger(level=logging.DEBUG):
    """
    helper for quickly adding a StreamHandler to the logger.
    useful for debugging.

    returns handler after adding it.
    """

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    legger.addHandler(handler)
    logger.setLevel(level)
    logger.debug(
        'added a stderr logging handler to logger: {}'.format(__name__))
    return handler

# ... cleanup (from urllib3, don't quite know why this is...)
del NullHandler
