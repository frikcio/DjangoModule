from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True)
    purse = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    image = models.ImageField(upload_to="photo")
    about = models.TextField()
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Purchase(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.DO_NOTHING, related_name="purchases")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="purchases")
    count = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product}"


class Return(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(ShopUser, on_delete=models.DO_NOTHING, related_name="returns")

    def __str__(self):
        return self.purchase.product
