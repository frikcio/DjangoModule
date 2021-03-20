from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from .models import ShopUser
from .shop_forms import RegisterForm


def home(request):
    return render(request, "index.html")


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/profile/{}/'.format(self.request.user.id)


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = '/login/'


class Profile(LoginRequiredMixin, DetailView):
    pk_url_kwarg = "pk"
    model = ShopUser
    template_name = "profile.html"

