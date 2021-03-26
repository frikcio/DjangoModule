import datetime
import pdb

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import ShopUser, ProductModel, PurchaseModel, ReturnModel
from .shop_forms import RegisterForm, AppendForm, BuyForm, ReturnForm


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


class Return(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = ReturnForm

    def form_valid(self, form):
        time = timezone.now().timestamp()
        purchase = PurchaseModel.objects.get(pk=self.kwargs["pk"])
        if (purchase.date + datetime.timedelta(minutes=3)).timestamp() > time:
            user = self.request.user
            purchase.status = True
            purchase.save()
            purchase_return = form.save(commit=False)
            purchase_return.purchase = purchase
            purchase_return.user = user
            purchase_return.save()
            return super().form_valid(form=form)
        else:
            purchase.return_status = True
            purchase.save()
            messages.info(self.request, "time is up")
            return redirect("/user/purchases/")

    def get_success_url(self):
        return "/user/purchases/"

    def form_invalid(self, form):
        messages.error(self.request, "Error")
        return redirect("/")


class Reject(DeleteView):
    model = ReturnModel
    success_url = "/products/returns/"

    def delete(self, request, success_url=success_url, *args, **kwargs):
        return_object = self.get_object()
        purchase = return_object.purchase
        purchase.return_status = True
        purchase.save()
        return_object.delete()
        return HttpResponseRedirect(success_url)



class Accept(DeleteView):
    model = PurchaseModel
    success_url = "/products/returns/"

    def delete(self, request, success_url=success_url, *args, **kwargs):
        purchase_object = self.get_object()
        product = purchase_object.product
        user = purchase_object.user
        user.purse += product.price * purchase_object.count
        product.count += purchase_object.count
        user.save()
        product.save()
        purchase_object.delete()
        return HttpResponseRedirect(success_url)


class ReturnHandler(ListView):
    model = ReturnModel
    template_name = "returns.html"
    paginate_by = 5


class PurchasesList(ListView):
    model = PurchaseModel
    template_name = "purchases.html"
    extra_context = {"form": ReturnForm}
    paginate_by = 5


class Profile(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    pk_url_kwarg = "pk"
    model = ShopUser
    template_name = "profile.html"


class ProductListView(ListView):
    model = ProductModel
    template_name = 'index.html'
    paginate_by = 5


class ProductAppend(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = AppendForm
    template_name = "add_product.html"
    success_url = '/'


class ProductUpdate(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    template_name = "change_product.html"
    model = ProductModel
    fields = ["name", "image", "about", "price", "count"]

    def get_success_url(self):
        return "/about/{}".format(self.object.pk)


class ProductAbout(DetailView):
    model = ProductModel
    template_name = "product.html"
    extra_context = {"form": BuyForm}


class ProductBuy(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = BuyForm

    def form_valid(self, form):
        product = ProductModel.objects.get(pk=self.kwargs["pk"])
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
        elif product.count < form.cleaned_data["count"]:
            messages.error(self.request, "not so match")
            return redirect(f"/product/about/{self.kwargs['pk']}")
        elif user.purse < (product.price*form.cleaned_data["count"]):
            messages.error(self.request, "not enough money")
            return redirect(f"/product/about/{self.kwargs['pk']}")

    def get_success_url(self):
        return "/user/purchases"

    def form_invalid(self, form):
        messages.error(self.request, "product count must be more than 0")
        return redirect(f"/product/about/{self.kwargs['pk']}")
