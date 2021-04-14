import pdb

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.migrations import exceptions
from django.utils import timezone
from rest_framework.authtoken.models import Token

from base.my_exseptions import NotMuchCount, NotMuchMoney, NotZeroCount


class ShopUser(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True)
    purse = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.username


class ProductModel(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    image = models.ImageField(blank=True, null=True)
    about = models.TextField()
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PurchaseModel(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.DO_NOTHING, related_name="purchases")
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING, related_name="purchases")
    count = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    return_status = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        need_count = self.count
        if self.product.count >= need_count and self.user.purse >= (
                self.product.price * need_count) and need_count != 0:
            self.product.count -= need_count
            self.user.purse -= (self.product.price * need_count)
            with transaction.atomic():
                self.user.save()
                self.product.save()
                super(PurchaseModel, self).save(*args, **kwargs)
        elif self.product.count < need_count:
            raise NotMuchCount()
        elif self.user.purse < (self.product.price * need_count):
            raise NotMuchMoney()
        elif need_count == 0:
            raise NotZeroCount()

    def __str__(self):
        return f"{self.product}"


class ReturnModel(models.Model):
    purchase = models.ForeignKey(PurchaseModel, on_delete=models.CASCADE, related_name="returns")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ShopUser, on_delete=models.DO_NOTHING, related_name="returns")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.purchase}"


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=120)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="book")

    def __str__(self):
        return self.title


class TemporaryToken(Token):
    last_action = models.DateTimeField(null=True)
