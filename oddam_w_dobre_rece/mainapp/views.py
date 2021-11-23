from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View

from mainapp.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request):
        stat_passed_bags = 0
        for item in Donation.objects.all():
            stat_passed_bags += item.quantity
        stat_supported_institutions = Donation.objects.all().count()
        foundations = Institution.objects.filter(type=0)
        organizations = Institution.objects.filter(type=1)
        local_collections = Institution.objects.filter(type=2)
        f_page = request.GET.get('f_page')
        o_page = request.GET.get('o_page')
        c_page = request.GET.get('c_page')
        p_foundations = Paginator(foundations, 1)
        p_foundations_page = p_foundations.get_page(f_page)
        p_organization = Paginator(organizations, 1)
        p_organization_page = p_organization.get_page(o_page)
        p_collections = Paginator(local_collections, 1)
        p_collections_page = p_collections.get_page(c_page)
        return render(request, 'index.html',
                      {'stat_bags': stat_passed_bags, 'stat_institutions': stat_supported_institutions,
                       'foundations': foundations, 'organizations': organizations, 'collections': local_collections,
                       'p_foundation': p_foundations_page, 'p_organization': p_organization_page,
                       'p_collections': p_collections_page, 'request': request
                       })


class AddDonation(LoginRequiredMixin, View):
    login_url = '/login/#login'

    def get(self, request):
        institutions = Institution.objects.all()
        categories = Category.objects.all()
        return render(request, 'form.html', {
            'institutions': institutions, 'categories': categories
        })


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        try:
            if User.objects.get(username=request.POST.get('email')):
                user = authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
                login(request, user)
                return redirect(reverse_lazy('landing_page'))
            else:
                return redirect(reverse_lazy('login'))
        except User.DoesNotExist:
            return redirect(reverse('register'))


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('landing_page'))


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        email = request.POST.get('email')
        if request.POST.get('password') == request.POST.get('password2'):
            User.objects.create_user(username=email, email=email, password=request.POST.get('password'),
                                     first_name=first_name, last_name=last_name)
            return redirect(reverse_lazy('login'))
        else:
            return render(request, 'register.html', {'error_message': 'Wprowadzone hasła są różne!'})
