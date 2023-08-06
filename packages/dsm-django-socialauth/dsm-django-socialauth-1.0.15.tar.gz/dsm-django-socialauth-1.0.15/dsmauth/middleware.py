from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTauthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _user = JWTAuthentication().authenticate(request)
        request.user = _user[0] if _user != None else request.user