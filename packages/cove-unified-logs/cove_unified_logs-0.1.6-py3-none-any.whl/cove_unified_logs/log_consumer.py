# log_consumer.py
import json
import uuid

import redis
import logging
import os
from cove_unified_logs.cloud_logger import CloudLogger


class LogConsumer:
    def __init__(self, channel='logs', cloud_logger=None):
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_password = os.getenv('REDIS_PASSWORD', None)
        try:
            if redis_password is not None:
                self.redis = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
            else:
                self.redis = redis.Redis(host=redis_host, port=redis_port)
            self.pubsub = self.redis.pubsub()
            self.pubsub.subscribe(channel)
            self.cloud_logger = cloud_logger
        except Exception as e:
            logging.error(f"Failed to initialize LogConsumer: {str(e)}")
            raise

    def run(self):
        try:
            for item in self.pubsub.listen():
                if item['type'] == 'message':
                    log_event = json.loads(item['data'])
                    self.cloud_logger._put_log_event(
                        log_event['level'],
                        log_event['message'],
                        **log_event['metadata']
                    )
                    self.cloud_logger.flush()
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Failed to consume log event due to Redis connection error: {str(e)}")
            # exit failure, so that docker can restart the container
            exit(1)
            # handle connection error, for example by retrying or by failing gracefully
        except Exception as e:
            logging.error(f"Failed to consume log event: {str(e)}")
            # exit failure, so that docker can restart the container
            exit(1)
            # handle unexpected errors

'''
#usage
from cove_unified_logs.log_consumer import LogConsumer
from cove_unified_logs.cloud_logger import CloudLogger
cloud_logger = CloudLogger(group_name='log-group', stream_name='log-stream', region_name='eu-west-1', flush_interval=10, batch_size=100)
consumer = LogConsumer(cloud_logger=cloud_logger)
consumer.run()
'''