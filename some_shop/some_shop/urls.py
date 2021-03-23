from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name="django_admin"),
    path("", include("base.urls"))
]
