from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from base.models import ShopUser, ProductModel, PurchaseModel, ReturnModel


class RegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ["username", ]


class AppendForm(ModelForm):
    class Meta:
        model = ProductModel
        exclude = ["image"]


class BuyForm(ModelForm):
    class Meta:
        model = PurchaseModel
        fields = ["count"]


class ReturnForm(ModelForm):
    class Meta:
        model = ReturnModel
        fields = []
