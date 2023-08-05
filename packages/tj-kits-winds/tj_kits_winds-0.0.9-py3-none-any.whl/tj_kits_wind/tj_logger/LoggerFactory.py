import logging
import logging.config
import os
import sys
from typing import AnyStr, Dict, Optional, Literal, Union

__all__ = ['FORMAT_VERY_SHORT', 'FORMAT_SHORT', 'FORMAT_NORMAL', 'FORMAT_WORDY',
           'LOG_DEBUG', 'LOG_INFO', 'LOG_WARNING', 'LOG_ERROR', 'LOG_CRITICAL',
           'logger_console', 'logger_auto']

FORMAT_VERY_SHORT = "very_short"
FORMAT_SHORT = "short"
FORMAT_NORMAL = "normal"
FORMAT_WORDY = "wordy"
LOGGER_FORMAT = Union[FORMAT_VERY_SHORT, FORMAT_SHORT, FORMAT_NORMAL, FORMAT_WORDY]

LOG_DEBUG = "DEBUG"
LOG_INFO = "INFO"
LOG_WARNING = "WARNING"
LOG_ERROR = "ERROR"
LOG_CRITICAL = "CRITICAL"
LOGGER_LEVEL = Union[LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR, LOG_CRITICAL]


def get_logger_conf_dict() -> Dict:
    LOGGER_CONF = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            "main": {
                "datefmt": '%m-%d %H:%M:%S',
                # "format": "[%(asctime)s | %(levelname)s | pid:%(process)d | %(filename)s:%(lineno)d] %(message)s"

            },
        },

        #
        "handlers": {
            'tj_c': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
                'formatter': 'main'
            },
        },

        #
        "loggers": {
            # 配置文件 中 只要定义了 root logger 就一定会 先传递至 root
            #  其他 logger 均相当其 子类, 无论配置是否扩散
            # "root": {
            #     'handlers': ["tj_c"],
            #     'level': "DEBUG",
            #     "propagate": 1,
            # },
            "tj_c": {
                'handlers': ["tj_c"],
                'level': "DEBUG",
            },
        }
    }

    return LOGGER_CONF


def logger_console(logger_format: LOGGER_FORMAT = "short"):
    return create_logger("tj_c", logger_format=logger_format)


def logger_auto(name: AnyStr, log_path: AnyStr, logger_format: LOGGER_FORMAT = "normal",
                max_mb: int = 100, back_up_count: int = 10):
    add_handler = {
        'encoding': 'utf8',
        'level': 'DEBUG',
        'class': 'logging.handlers.RotatingFileHandler',
        'maxBytes': 1024 * 1024 * max_mb,  # 100MB
        'backupCount': back_up_count,  # 100MB * 10 = 1G
        'formatter': 'main',
        'filename': ""
    }

    add_logger = {
        'handlers': [name],
        'level': "DEBUG",
    }

    return create_logger(name, file_name="{}.log".format(name), log_path=log_path, add_handler=add_handler,
                         add_logger=add_logger, logger_format=logger_format)


def create_logger(name: AnyStr,
                  file_name: AnyStr = "tj.log",
                  log_path: AnyStr = "/tmp/tj_log",
                  add_handler: Optional[Dict] = None,
                  add_logger: Optional[Dict] = None,
                  logger_format: LOGGER_FORMAT = "normal",
                  level: LOGGER_LEVEL = "INFO"):
    LOGGER_CONF = get_logger_conf_dict()

    # 1. add handler and logger
    if add_handler:
        LOGGER_CONF["handlers"][name] = add_handler
    if add_logger:
        LOGGER_CONF["loggers"][name] = add_logger

    # 2. set format and level
    if logger_format == "very_short":
        LOGGER_CONF["formatters"]["main"]["format"] = "[%(levelname)s] %(message)s"
    if logger_format == "short":
        LOGGER_CONF["formatters"]["main"]["format"] = "[%(asctime)s | %(levelname)s] %(message)s"
    if logger_format == "normal":
        LOGGER_CONF["formatters"]["main"]["format"] = \
            "[%(asctime)s | %(levelname)s | pid:%(process)d | %(filename)s:%(lineno)d] %(message)s"
    if logger_format == "wordy":
        LOGGER_CONF["formatters"]["main"]["format"] = \
            "[%(asctime)s | %(levelname)s | pid:%(process)d | tid:%(thread)d | %(module)s | %(funcName)s | %(filename)s:%(lineno)d] %(message)s"

    # 设置 level & mkdir file_path
    LOGGER_CONF["handlers"][name]["level"] = level
    if "filename" in LOGGER_CONF["handlers"][name].keys():
        if not os.path.isdir(log_path):
            os.makedirs(log_path)

        LOGGER_CONF["handlers"][name]["filename"] = "{}/{}".format(log_path, file_name)

    # 确定 logger name
    logger_name = LOGGER_CONF["loggers"].keys()
    if not name:
        name = "tj_c"

    # 返回 logger
    logging.config.dictConfig(LOGGER_CONF)
    logger = logging.getLogger(name)

    return logger
