from django.shortcuts import render

# Create your views here.
from django.views import View

from mainapp.models import Donation


class LandingPage(View):
    def get(self, request):
        stat_passed_bags = 0
        for item in Donation.objects.all():
            stat_passed_bags += item.quantity
        stat_supported_institutions = Donation.objects.all().count()
        return render(request, 'index.html',
                      {'stat_bags': stat_passed_bags, 'stat_institutions': stat_supported_institutions})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')
