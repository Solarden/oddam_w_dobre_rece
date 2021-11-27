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

    def post(self, request):
        donation = Donation.objects.create(quantity=request.POST.get('bags'), institution=Institution.objects.get(
            pk=int(request.POST.get('organization'))), address=request.POST.get('address'),
                                           phone_no=request.POST.get('phone'), city=request.POST.get('city'),
                                           zip_code=request.POST.get('postcode'),
                                           pick_up_date=request.POST.get('data'),
                                           pick_up_time=request.POST.get('time'),
                                           pick_up_comment=request.POST.get('more_info'), user=request.user)
        donation.categories.set(request.POST.get('categories'))
        return render(request, 'form-confirmation.html')


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


class UserInfo(View):
    def get(self, request):
        donations = Donation.objects.filter(user=request.user).order_by('is_taken')
        return render(request, 'user_info.html', {'donations': donations})

    def post(self, request):
        donations = Donation.objects.filter(user=request.user).order_by('is_taken')
        for i in Donation.objects.all():
            y = Donation.objects.get(pk=i.pk)
            if request.POST.get('is_taken' + str(i.pk)):
                y.is_taken = True
                y.save()
            elif not request.POST.get('is_taken' + str(i.pk)):
                y.is_taken = False
                y.save()
        return render(request, 'user_info.html', {'error_message': 'Zapisano zmiany!', 'donations': donations})
