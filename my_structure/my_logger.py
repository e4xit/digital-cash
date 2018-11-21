##########
# Logger #
##########

import logging

import globalconfig

logging.basicConfig(
    level="INFO",
    format='%(threadName)-6s | %(message)s',
)
logger = logging.getLogger(__name__)
