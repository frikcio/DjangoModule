from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from base.API.serializers import AuthorSerializer, BookSerializer, AuthorBooksSerializer, PurchaseSerializer, \
    ProductSerializer
from base.authentication import TemporaryTokenAuth
from base.models import Author, Book, TemporaryToken, PurchaseModel, ProductModel
from base.my_exseptions import NotMuchMoney, NotMuchCount, NotZeroCount
from some_shop import settings


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def list(self, request, *args, **kwargs):
        if request.query_params:
            queryset = Author.objects.all().filter(book__title__contains=request.query_params["book_name"])
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def get_books(self, request, pk):
        author = self.get_object()
        serializer = AuthorBooksSerializer(author)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        if request.query_params:
            queryset = Book.objects.all().filter(author__age__lte=request.query_params["author_age"])
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(title=serializer.validated_data["title"]+"!")


class AuthorizationView(APIView):
    authentication_classes = [BasicAuthentication, TemporaryTokenAuth]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {
            "user": request.user.username,
            "token": request.auth.key,
        }
        return Response(content)


class GetToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = TemporaryToken.objects.get_or_create(user=user)
        if token.last_action and (timezone.now() - token.last_action) > settings.TOKEN_LIFETIME * 60:
            token = TemporaryToken.objects.update(user=user)
        return Response({'token': token.key})


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, TemporaryTokenAuth]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, TemporaryTokenAuth]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = PurchaseModel.objects.all()
    serializer_class = PurchaseSerializer

    def list(self, request, *args, **kwargs):
        if request.query_params:
            queryset = PurchaseModel.objects.filter(user=self.request.user)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        product = ProductModel.objects.get(pk=serializer.validated_data["product"].pk)
        try:
            serializer.save(user=self.request.user, product=product)
        except NotMuchMoney:
            raise exceptions.APIException("You have not enough money")
        except NotMuchCount:
            raise exceptions.APIException("We have not enough product's count")
        except NotZeroCount:
            raise exceptions.APIException("product count must be more than 0")
