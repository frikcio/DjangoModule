from django.contrib.auth.forms import UserCreationForm

from base.models import ShopUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ["username", ]
