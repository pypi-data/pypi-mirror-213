import boto3
import logging
import json
import time
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from botocore.exceptions import BotoCoreError, ClientError

class CloudLogger:
    _instance = None
    _lock = threading.Lock()  # Class level lock for thread-safe singleton

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(CloudLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, group_name, stream_name, region_name=None, flush_interval=10, batch_size=100):
        if not hasattr(self, 'initialized'):
            self.group_name = group_name
            self.stream_name = stream_name
            self.sequence_token = None
            self.log_events = []
            self.lock = threading.Lock()
            self.flush_interval = flush_interval
            self.batch_size = batch_size

            # Create session and CloudWatch client
            if region_name is None:
                region_name = boto3.Session().region_name
            session = boto3.Session(region_name=region_name)
            self.client = session.client('logs')

            # Create or get log group and stream
            self._initialize_log_group()
            self._initialize_log_stream()

            self.initialized = True

            # Start the automatic flushing thread
            self.stop_flush_thread = threading.Event()
            self.flush_thread = threading.Thread(target=self._auto_flush)
            self.flush_thread.start()
            self.executor = ThreadPoolExecutor(max_workers=5)  # or any number you prefer for max_workers

    def _initialize_log_group(self):
        try:
            self.client.create_log_group(logGroupName=self.group_name)
            logging.info(f"Log group {self.group_name} created successfully.")
        except self.client.exceptions.ResourceAlreadyExistsException:
            logging.info(f"Log group {self.group_name} already exists.")
        except (BotoCoreError, ClientError) as e:
            logging.error("Failed to create log group", exc_info=True)

    def _initialize_log_stream(self):
        try:
            response = self.client.describe_log_streams(
                logGroupName=self.group_name,
                logStreamNamePrefix=self.stream_name
            )
            if not response['logStreams']:
                self.client.create_log_stream(
                    logGroupName=self.group_name,
                    logStreamName=self.stream_name
                )
                logging.info(f"Log stream {self.stream_name} created successfully.")
            else:
                self.sequence_token = response['logStreams'][0].get('uploadSequenceToken')
                logging.info(f"Log stream {self.stream_name} already exists. Using sequence token {self.sequence_token}")
        except (BotoCoreError, ClientError) as e:
            logging.error("Failed to initialize log stream", exc_info=True)

    def _put_log_event(self, level, message, **metadata):
        with self.lock:
            try:
                log_event = {
                    'timestamp': metadata.pop('timestamp', int(time.time() * 1000)),
                    'message': json.dumps({
                        'level': level,
                        'message': message,
                        'metadata': metadata
                    })
                }
                self.log_events.append(log_event)

                if len(self.log_events) >= self.batch_size:
                    self._flush()

            except (BotoCoreError, ClientError) as e:
                logging.error("Failed to put log event", exc_info=True)

    def _auto_flush(self):
        while not self.stop_flush_thread.is_set():
            time.sleep(self.flush_interval)
            self._flush()
            print("===flushed")

    def _flush(self):
        with self.lock:
            if self.log_events:
                try:
                    kwargs = {
                        'logGroupName': self.group_name,
                        'logStreamName': self.stream_name,
                        'logEvents': self.log_events
                    }
                    if self.sequence_token:
                        kwargs['sequenceToken'] = self.sequence_token

                    response = self.client.put_log_events(**kwargs)
                    print("===kwargs:", kwargs)
                    print("===response:", response)
                    self.sequence_token = response['nextSequenceToken']
                    self.log_events.clear()
                except self.client.exceptions.DataAlreadyAcceptedException:
                    logging.warning("DataAlreadyAcceptedException occurred.")
                except self.client.exceptions.InvalidSequenceTokenException:
                    logging.warning("InvalidSequenceTokenException occurred.")
                except (BotoCoreError, ClientError) as e:
                    logging.error("Failed to flush log events", exc_info=True)

    def debug(self, message, **metadata):
        self.executor.submit(self._put_log_event, 'debug', message, **metadata)

    def info(self, message, **metadata):
        self.executor.submit(self._put_log_event, 'info', message, **metadata)

    def warning(self, message, **metadata):
        self.executor.submit(self._put_log_event, 'warning', message, **metadata)

    def error(self, message, **metadata):
        self.executor.submit(self._put_log_event, 'error', message, **metadata)

    def critical(self, message, **metadata):
        self.executor.submit(self._put_log_event, 'critical', message, **metadata)

    def flush(self):
        self._flush()

    def close(self):
        self.stop_flush_thread.set()  # Stop the flush thread
        self.flush_thread.join()  # Wait for the flush thread to finish
        self._flush()  # Flush any remaining logs
        self.executor.shutdown(wait=True)
