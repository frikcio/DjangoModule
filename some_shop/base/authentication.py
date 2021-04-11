from rest_framework.authentication import TokenAuthentication

from base.models import TemporaryToken


class TemporaryTokenAuth(TokenAuthentication):
    model = TemporaryToken

    def authenticate(self, request):
        inter_value = super().authenticate(request=request)
        if inter_value:
            user, token = inter_value
            return user, token
