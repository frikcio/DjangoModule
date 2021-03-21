from django.contrib import admin


# Register your models here.
from base.models import Product
from base.models import ShopUser

admin.site.register(Product)
admin.site.register(ShopUser)
