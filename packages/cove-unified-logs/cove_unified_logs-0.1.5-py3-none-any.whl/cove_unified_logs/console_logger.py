import logging

class ConsoleLogger:
    def __init__(self, app_name: str):
        self.app_name = app_name
        # Configure logger
        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.DEBUG)
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(app_name)s - %(levelname)s - %(message)s - %(metadata)s'
        )
        console_handler.setFormatter(formatter)
        # Add the console handler to the logger
        self.logger.addHandler(console_handler)

    def _put_log_event(self, level, message, **metadata):
        # Log the message
        self.logger.log(level, message, extra={'app_name': self.app_name, 'metadata': metadata})

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
        # Log the exception with a traceback
        self.logger.exception(message, extra={'app_name': self.app_name, 'metadata': metadata})
