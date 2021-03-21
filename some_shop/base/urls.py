
from django.urls import path

from .views import *

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("profile/<int:pk>/", Profile.as_view(), name="profile"),
    path("add_product/", ProductAppend.as_view(), name="append"),
    path("about/<int:pk>/", ProductAbout.as_view(), name="about"),
    path("change_product/<int:pk>", ProductUpdate.as_view(), name="change_product"),
    path("buy_pruduct/<int:pk>", ProductBuy.as_view(), name="buy_product")
]
