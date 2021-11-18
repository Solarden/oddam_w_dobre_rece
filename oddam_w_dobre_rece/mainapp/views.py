from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.
from django.views import View

from mainapp.models import Donation, Institution


class LandingPage(View):
    def get(self, request):
        stat_passed_bags = 0
        for item in Donation.objects.all():
            stat_passed_bags += item.quantity
        stat_supported_institutions = Donation.objects.all().count()
        foundations = Institution.objects.filter(type=0)
        organizations = Institution.objects.filter(type=1)
        local_collections = Institution.objects.filter(type=2)
        p_foundations = Paginator(foundations, 1)
        f_page = request.GET.get('f_page')
        o_page = request.GET.get('o_page')
        p_foundations_page = p_foundations.get_page(f_page)
        p_organization = Paginator(organizations, 1)
        p_organization_page = p_organization.get_page(o_page)
        p_collections = Paginator(local_collections, 1)
        p_collections_page = p_collections.get_page(o_page)
        return render(request, 'index.html',
                      {'stat_bags': stat_passed_bags, 'stat_institutions': stat_supported_institutions,
                       'foundations': foundations, 'organizations': organizations, 'collections': local_collections,
                       'p_foundation': p_foundations_page, 'p_organization': p_organization_page})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')
