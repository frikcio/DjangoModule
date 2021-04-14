from rest_framework import serializers
from base.models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "age"]


class AuthorBooksSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "age", "book"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author"]


class UserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source=ShopUser.username)

    class Meta:
        model = ShopUser
        fields = ["id", "user", "purse"]


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseModel
        fields = ["id", "product", "count", "date"]


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnModel
        fields = ["id", "user", "purchase", "date"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ["id", "name", "price", "count"]
