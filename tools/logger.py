import atexit
import logging
import logging.config
import sys
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from logging import Formatter
from pathlib import Path
from queue import Queue
from typing import Any, Dict, List
import os

import yaml

from pythonjsonlogger.jsonlogger import JsonFormatter  # type: ignore

# init root logger with null handler
logging.basicConfig(handlers=[logging.NullHandler()])

# init log queue for handler and listener
log_queue: Queue = Queue()
log_qlistener: QueueListener = QueueListener(log_queue, respect_handler_level=True)
log_qlistener.start()
atexit.register(log_qlistener.stop)


class StackDriverFormatter(JsonFormatter):
    def process_log_record(self, log_record: Dict[str, Any]) -> Dict[str, Any]:
        log_record["severity"] = log_record["levelname"]
        return super().process_log_record(log_record)


def _get_log_formatter(json_format: bool = False) -> Formatter:
    # formatter
    log_format = "%(asctime)s [%(processName)s-%(threadName)s] %(levelname)s %(name)s %(filename)s:%(lineno)d : %(message)s"

    date_format = "%Y-%m-%dT%H:%M:%S"
    if json_format:
        return StackDriverFormatter(
            fmt=log_format, datefmt=date_format, timestamp=True
        )
    return Formatter(log_format)


def _get_file_handler(
    log_path: str = "main.log", log_level: int = logging.DEBUG, json_format: bool = False
) -> RotatingFileHandler:
    _tmp_path = os.path.dirname(os.path.abspath(__file__))
    _tmp_path = os.path.join(_tmp_path, log_path)
    log_dir = os.path.dirname(_tmp_path)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=2 ** 20,  # 1 MB
        backupCount=10,  # 10 backup
        encoding="utf8",
        delay=True,
    )

    file_handler.setLevel(log_level)
    file_handler.setFormatter(_get_log_formatter(json_format))
    return file_handler


def _get_stdout_handler(log_level: int = logging.INFO, json_format: bool = False) -> logging.StreamHandler:
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(_get_log_formatter(json_format))
    return stdout_handler


class QueueListenerHandler(QueueHandler):
    def __init__(self, handlers):
        super().__init__(Queue())
        self._start_listener(self.queue, handlers)

    def _start_listener(self, queue, handlers) -> QueueListener:
        self.listener = QueueListener(queue, *handlers, respect_handler_level=True)
        self.listener.start()
        atexit.register(self.listener.stop)
        return self.listener


def configure_log_listener(
    console: bool = True, log_path: str = "./main.log", json_format: bool = False
) -> QueueListener:
    """
    Configure log queue listener to log into file and console.
    Args:
        console (bool): whether to log on console
        log_path (str): path of log file
    Returns:
        log_qlistener (logging.handlers.QueueListener): configured log queue listener
    """
    global log_qlistener
    try:
        atexit.unregister(log_qlistener.stop)
        log_qlistener.stop()
    except (AttributeError, NameError):
        pass

    handlers: List[logging.Handler] = []

    # rotating file handler
    if log_path:
        file_handler = _get_file_handler(log_path, json_format)
        handlers.append(file_handler)

    # console handler
    if console:
        stdout_handler = _get_stdout_handler(json_format)
        handlers.append(stdout_handler)

    log_qlistener = QueueListener(log_queue, *handlers, respect_handler_level=True)
    log_qlistener.start()
    atexit.register(log_qlistener.stop)
    return log_qlistener


def configure_loggers(conf_yaml: str = "logging.yml") -> None:
    """
    Configure loggers with configurations defined in yaml
    Args:
        conf_yaml: path of yaml config file
    """
    log_conf = yaml.safe_load(Path(conf_yaml).read_text())
    logging.config.dictConfig(log_conf)


def get_logger(name: str = 'default', log_path: str = './logs/default.log', log_level: int = logging.DEBUG, json_format: bool = False) -> logging.Logger:
    """
    Simple logging wrapper that returns logger
    configured to log into file and console.
    Args:
        :param json_format:
        :param log_level:
        :param name:
        :param log_path:
    Returns:
        logger: configured logger

    """
    logger_create = logging.getLogger(name)
    for log_handler in logger_create.handlers[:]:
        logger_create.removeHandler(log_handler)

    logger_create.setLevel(log_level)
    logger_create.addHandler(QueueHandler(log_queue))

    configure_log_listener(True, log_path, json_format)

    return logger_create
