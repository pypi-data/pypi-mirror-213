from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

import logging


User = get_user_model()


class AutoCreateUserFromTokenMiddleware(MiddlewareMixin):
    """
    Middleware for auto creating user from JWToken.
    It parses token, gets 'user' field and creates/updates user with data from this field.
    """
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            return self.get_response(request)
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        if not token:
            return self.get_response(request)
        try:
            algorithm = settings.SIMPLE_JWT['ALGORITHM']
            user_data = jwt_decode(token, settings.SECRET_KEY, algorithms=[algorithm])['user']
        except (InvalidToken, TokenError) as e:
            logging.error(e)
            return self.get_response(request)
        else:
            defaults = user_data
            user, user_created = get_user_model().objects.update_or_create(
                id=user_data['id'],
                defaults=defaults
            )
            request.user = user
            return self.get_response(request)
