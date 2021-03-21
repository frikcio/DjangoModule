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
        product_count = Purchase.objects.get()
        product_price = Purchase.product.price
        user_money = Purchase.user.purse
        if need_count > product_count:
            self.add_error("count", "to mach")
        if product_price > user_money:
            self.add_error(None, "not much money")
