from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from base.models import TemporaryToken
from some_shop import settings


class TemporaryTokenAuth(TokenAuthentication):
    model = TemporaryToken

    def authenticate(self, request):
        inter_value = super().authenticate(request=request)
        if inter_value:
            user, token = inter_value
            if token.last_action and (timezone.now() - token.last_action) > settings.TOKEN_LIFETIME*60:
                msg = "Token's lifetime is ended"
                raise exceptions.AuthenticationFailed(msg)
            token.last_action = timezone.now()
            return user, token
