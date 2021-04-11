from rest_framework import serializers
from base.models import Author, Book, ShopUser


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
