import boto3
import logging
import json
from concurrent.futures import ThreadPoolExecutor
import time

class CloudLogger:
    def __init__(self, group_name, stream_name):
        self.group_name = group_name
        self.stream_name = stream_name
        self.sequence_token = None

        # create CloudWatch client
        self.client = boto3.client('logs')

        # create thread pool executor
        self.executor = ThreadPoolExecutor(max_workers=5)

        # create or get log group and stream
        self._initialize_log_group()
        self._initialize_log_stream()

    def _initialize_log_group(self):
        try:
            self.client.create_log_group(logGroupName=self.group_name)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass

    def _initialize_log_stream(self):
        try:
            self.client.create_log_stream(logGroupName=self.group_name, logStreamName=self.stream_name)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass

    def _put_log_event(self, level, message, **metadata):
        response = self.client.put_log_events(
            logGroupName=self.group_name,
            logStreamName=self.stream_name,
            logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': json.dumps({
                        'level': level,
                        'message': message,
                        'metadata': metadata
                    })
                }
            ],
            sequenceToken=self.sequence_token
        )
        self.sequence_token = response['nextSequenceToken']

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
