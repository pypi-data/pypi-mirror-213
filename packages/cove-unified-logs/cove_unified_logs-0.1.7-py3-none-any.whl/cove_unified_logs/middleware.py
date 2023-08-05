# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.apps import apps
from .unified_logger import UnifiedLogger

class LoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.app_name = apps.get_app_config(__package__.split('.')[0]).verbose_name
        self.logger = UnifiedLogger(self.app_name, config='all')
        self.logger.set_level(settings.LOG_LEVEL)

    def process_request(self, request):
        self.logger.debug('Request received', path=request.path)

    def process_response(self, request, response):
        self.logger.debug('Response sent', status_code=response.status_code)
        return response

    def process_exception(self, request, exception):
        self.logger.error('Exception encountered', exception=str(exception))
