from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls, name="django_admin"),
    path("accounts/", include("accounts.urls")),
    path("core/", include("core.urls")),
]
