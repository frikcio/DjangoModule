
from django.urls import path

from .views import home, Login, Register, Logout, Profile

urlpatterns = [
    path("", home, name="home"),
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("profile/<int:pk>/", Profile.as_view(), name="profile")
]
