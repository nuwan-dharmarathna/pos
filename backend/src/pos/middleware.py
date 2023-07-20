from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.middleware import get_user

class CashierNameMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = get_user(request)
        if user.is_authenticated and not request.user.is_staff:
            request.cashier = user

