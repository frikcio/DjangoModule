import pdb

from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from base.models import ShopUser, Product, Purchase


class RegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ["username", ]


class AppendForm(ModelForm):
    class Meta:
        model = Product
        exclude = []


class BuyForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ["count"]

    def clean(self):
        cleaned_data = super().clean()
        need_count = cleaned_data.get("count")
        if not need_count > 0:
            self.add_error("count", f"count must be more than {need_count}")


