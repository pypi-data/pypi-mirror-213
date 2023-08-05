import time

from .log_producer import LogProducer
from .console_logger import ConsoleLogger
import os


class UnifiedLogger:
    def __init__(self, config='all', app_name='cove', log_level=None):
        if log_level is None:
            log_level = os.environ.get('LOG_LEVEL', 'info')
        self.log_level = log_level.lower()
        self.app_name = app_name
        self.loggers = []
        if config in ('all', 'console'):
            self.loggers.append(ConsoleLogger())
        if config in ('all', 'cloud'):
            self.loggers.append(LogProducer())

    def _log(self, level, message, **metadata):
        metadata['app_name'] = metadata.pop('app_name', self.app_name)
        metadata['timestamp'] = int(time.time() * 1000)
        for logger in self.loggers:
            getattr(logger, level)(message, **metadata)

    def debug(self, message, **metadata):
        if self.log_level == 'debug':
            self._log('debug', message, **metadata)

    def info(self, message, **metadata):
        if self.log_level in ('debug', 'info'):
            self._log('info', message, **metadata)

    def warning(self, message, **metadata):
        if self.log_level in ('debug', 'info', 'warning'):
            self._log('warning', message, **metadata)

    def error(self, message, **metadata):
        if self.log_level in ('debug', 'info', 'warning', 'error'):
            self._log('error', message, **metadata)

    def critical(self, message, **metadata):
        if self.log_level in ('debug', 'info', 'warning', 'error', 'critical'):
            self._log('critical', message, **metadata)
