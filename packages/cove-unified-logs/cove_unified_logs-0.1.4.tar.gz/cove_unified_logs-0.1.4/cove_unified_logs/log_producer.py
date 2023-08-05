# log_producer.py
import json
import time
import redis
import logging
import os


class LogProducer:
    def __init__(self, channel='logs'):
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = os.getenv('REDIS_PORT', 6379)
        redis_password = os.getenv('REDIS_PASSWORD', None)
        try:
            if redis_password is not None:
                self.redis = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
            else:
                self.redis = redis.Redis(host=redis_host, port=redis_port)
            self.channel = channel
        except Exception as e:
            logging.error(f"Failed to initialize LogProducer: {str(e)}")
            raise

    def log(self, level, message, **metadata):
        try:
            log_event = {
                'timestamp': int(time.time() * 1000),
                'level': level,
                'message': message,
                'metadata': metadata
            }
            self.redis.publish(self.channel, json.dumps(log_event))
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Failed to publish log event due to Redis connection error: {str(e)}")
            # handle connection error, for example by retrying or by failing gracefully
        except Exception as e:
            logging.error(f"Failed to publish log event: {str(e)}")
            # handle unexpected errors

    def debug(self, message, **metadata):
        self.log('debug', message, **metadata)

    def info(self, message, **metadata):
        self.log('info', message, **metadata)

    def warning(self, message, **metadata):
        self.log('warning', message, **metadata)

    def error(self, message, **metadata):
        self.log('error', message, **metadata)

    def critical(self, message, **metadata):
        self.log('critical', message, **metadata)

