import pdb

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import ShopUser, Product, Purchase, Return
from .shop_forms import RegisterForm, AppendForm, BuyForm


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/profile/{}/'.format(self.request.user.id)


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.purse = 10000
        obj.save()
        return super().form_valid(form=form)


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = '/login/'


class Returns(LoginRequiredMixin, CreateView):
    pk_url_kwarg = 'pk'
    login_url = "/login/"
    model = Return
    fields = []
    success_url = "/user/purchases/"
    template_name = "purchases.html"

    def form_valid(self, form):
        user = self.request.user
        obj = form.save(commit=False)
        obj.user = user
        obj.purchase = Purchase.objects.get(pk=self.kwargs["pk"])
        obj.save()
        return super().form_valid(form=form)


class PurchasesList(ListView):
    model = Purchase
    template_name = "purchases.html"


class Profile(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    pk_url_kwarg = "pk"
    model = ShopUser
    template_name = "profile.html"


class ProductListView(ListView):
    model = Product
    template_name = 'index.html'


class ProductAppend(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = AppendForm
    template_name = "add_product.html"
    success_url = '/'


class ProductUpdate(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    template_name = "change_product.html"
    model = Product
    fields = ["name", "image", "about", "price", "count"]

    def get_success_url(self):
        return "/about/{}".format(self.object.pk)


class ProductAbout(DetailView):
    pk_url_kwarg = "pk"
    model = Product
    template_name = "product.html"
    extra_context = {"form": BuyForm}


class ProductBuy(LoginRequiredMixin, CreateView):
    pk_url_kwarg = "pk"
    login_url = "/login/"
    form_class = BuyForm

    def form_valid(self, form):
        product = Product.objects.get(pk=self.kwargs["pk"])
        user = self.request.user
        if product.count >= form.cleaned_data["count"] and user.purse >= (product.price*form.cleaned_data["count"]):
            product.count -= form.cleaned_data["count"]
            user.purse -= (product.price*form.cleaned_data["count"])
            purchase = form.save(commit=False)
            purchase.user = user
            purchase.product = product
            user.save()
            product.save()
            purchase.save()
            return super().form_valid(form=form)
        else:
            return redirect(f"/about/{self.kwargs['pk']}")

    def get_success_url(self):
        return "/profile/{}".format(self.request.user.id)

    def form_invalid(self, form):
        return redirect(f"/about/{self.kwargs['pk']}")
