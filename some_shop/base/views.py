from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import ShopUser, Product, Purchase
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


class Profile(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    pk_url_kwarg = "pk"
    model = ShopUser
    template_name = "profile.html"


class ProductListView(ListView):
    model = Product
    template_name = 'index.html'


class ProductAbout(DetailView):
    pk_url_kwarg = "pk"
    model = Product
    template_name = "product.html"
    extra_context = {"buy": BuyForm}


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


class ProductBuy(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = BuyForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        self.request.user.purse -= self.object.price
        obj.save()
        return super().form_valid(form=form)

    def get_success_url(self):
        return "/profile/{}".format(self.request.user.id)


