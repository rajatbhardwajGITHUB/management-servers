from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token

class SetCSRFTokenMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Ensure CSRF token is set on every response
        get_token(request)
        return response
