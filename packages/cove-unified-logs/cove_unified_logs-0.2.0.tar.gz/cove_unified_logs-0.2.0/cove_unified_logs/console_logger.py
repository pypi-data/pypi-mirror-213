import logging
import time

from .singleton import SingletonMeta

class CustomFormatter(logging.Formatter):
    converter = time.gmtime  # or use time.localtime for local time, not UTC

    def format(self, record):
        # Convert timestamp from milliseconds to seconds
        timestamp = record.metadata.get('timestamp', 0) / 1000.0
        # Convert the timestamp to struct_time
        record.asctime = time.strftime('%Y-%m-%d %H:%M:%S', self.converter(timestamp))
        return super().format(record)



class ConsoleLogger(metaclass=SingletonMeta):
    def __init__(self):
        # Configure logger
        self.app_name = "cove_backend"
        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.DEBUG)
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        # Create formatter
        formatter = CustomFormatter(
            '%(asctime)s - %(app_name)s - %(levelname)s - %(message)s - %(metadata)s'
        )
        console_handler.setFormatter(formatter)
        # Add the console handler to the logger
        self.logger.addHandler(console_handler)

    def _put_log_event(self, level, message, **metadata):
        # Log the message
        app_name = metadata.pop('app_name', self.app_name)
        self.logger.log(level, message, extra={'app_name': app_name, 'metadata': metadata})

    def debug(self, message, **metadata):
        self._put_log_event(logging.DEBUG, message, **metadata)

    def info(self, message, **metadata):
        self._put_log_event(logging.INFO, message, **metadata)

    def warning(self, message, **metadata):
        self._put_log_event(logging.WARNING, message, **metadata)

    def error(self, message, **metadata):
        self._put_log_event(logging.ERROR, message, **metadata)

    def critical(self, message, **metadata):
        self._put_log_event(logging.CRITICAL, message, **metadata)

    def exception(self, message, **metadata):
        app_name = metadata.pop('app_name', self.app_name)
        # Log the exception with a traceback
        self.logger.exception(message, extra={'app_name': app_name, 'metadata': metadata})
