from rest_framework import viewsets, permissions
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from base.API.serializers import AuthorSerializer, BookSerializer, AuthorBooksSerializer
from base.models import Author, Book, TemporaryToken


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
    authentication_classes = [BasicAuthentication, TokenAuthentication]
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
        return Response({'token': token.key})
