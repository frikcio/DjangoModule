from django.contrib import admin


# Register your models here.
from base.models import ProductModel, PurchaseModel, ReturnModel
from base.models import ShopUser

admin.site.register(ProductModel)
admin.site.register(ShopUser)
admin.site.register(PurchaseModel)
admin.site.register(ReturnModel)
