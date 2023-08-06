import os
import sys

from loguru import logger

logger.remove()

_conf = {
    "handlers": [
        {
            "sink": sys.stdout,
            "enqueue": True,
            "format": "<d>{time:HH:mm:ss.SS}</d> <c>{name}</c> <level>[{level:^8}]</level> : {message}",
            "level": "DEBUG",
            "colorize": True,
        }
    ]
}


logger.configure(**_conf)
logger = logger.bind(file="")
