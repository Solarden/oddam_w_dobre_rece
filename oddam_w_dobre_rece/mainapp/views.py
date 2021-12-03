from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from .utils import generate_token
from mainapp.models import Donation, Institution, Category, SiteUser
from django.core.mail import EmailMessage
from django.conf import settings


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
            if SiteUser.objects.get(username=request.POST.get('email')):
                user = authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
                if user is not None:
                    if not user.is_email_verified:
                        return render(request, 'login.html',
                                      {'error_message': 'Twoje konto nie jest aktywne sprawdź swoją skrzynkę mailową!'})
                    else:
                        login(request, user)
                        return redirect(reverse_lazy('landing_page'))
                else:
                    return render(request, 'login.html',
                           {'error_message': 'Wprowadzono błędne dane!'})
            else:
                return redirect(reverse_lazy('login'))
        except SiteUser.DoesNotExist:
            return redirect(reverse('register'))


class Logout(LoginRequiredMixin, View):
    login_url = '/login/#login'

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
            pwd = request.POST.get('password')
            special_symbols = ['$', '@', '#', '%', '!']
            error_messages = []
            if len(pwd) < 8:
                error_messages.append('Wprowadzone hasło jest za krótkie minimum 8 znaków!')
                return render(request, 'register.html',
                              {'error_message': 'Wprowadzone hasło jest za krótkie minimum 8 znaków!'})
            elif not any(char.isdigit() for char in pwd):
                error_messages.append('Wprowadzone hasło powinno mieć przynajmniej jedną liczbę!')
                return render(request, 'register.html',
                              {'error_message': 'Wprowadzone hasło powinno mieć przynajmniej jedną liczbę!'})
            elif not any(char.isupper() for char in pwd):
                error_messages.append('Wprowadzone hasło powinno mieć przynajmniej jedną dużą literę!')
                return render(request, 'register.html',
                              {'error_message': 'Wprowadzone hasło powinno mieć przynajmniej jedną dużą literę!'})
            elif not any(char.islower() for char in pwd):
                error_messages.append('Wprowadzone hasło powinno mieć przynajmniej jedną małą literę!')
                return render(request, 'register.html',
                              {'error_message': 'Wprowadzone hasło powinno mieć przynajmniej jedną małą literę!'})
            elif not any(char in special_symbols for char in pwd):
                error_messages.append('Wprowadzone hasło powinno mieć przynajmniej jeden specjalny znak !@#$%.')
                return render(request, 'register.html', {
                    'error_message': 'Wprowadzone hasło powinno mieć przynajmniej jeden specjalny znak !@#$%.'})
            elif len(error_messages) > 0:
                return render(request, 'register.html', {'error_message': 'xd'})
            else:
                user = SiteUser.objects.create_user(username=email, email=email, password=request.POST.get('password'),
                                                    first_name=first_name, last_name=last_name)
                current_site = get_current_site(request)
                email_subject = 'Aktywuj swoje konto'
                email_body = render_to_string('activate.html', {'user': user, 'domain': current_site,
                                                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                                'token': generate_token.make_token(user)
                                                                })
                email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER,
                                     to=[user.email])
                email.send()
                # send_mail(email_subject, email_body, settings.EMAIL_FROM_USER, [user.email])
                return render(request, 'login.html',
                              {
                                  'error_message': 'Konto zostało zarejestrowane sprawdź skrzynkę pocztową w celu aktywacji'})
        else:
            return render(request, 'register.html', {'error_message': 'Wprowadzone hasła są różne!'})


class ActivateUser(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = SiteUser.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user and generate_token.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return render(request, 'login.html', {'error_message': 'Konto zostało aktywowane!'})
        return render(request, 'activate_failed.html', {'user': user})


class UserInfo(LoginRequiredMixin, View):
    login_url = '/login/#login'

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


class UserEdit(LoginRequiredMixin, View):
    login_url = '/login/#login'

    def get(self, request):
        return render(request, 'user_edit.html')

    def post(self, request):
        try:
            object = SiteUser.objects.get(email=request.POST.get('email'))
            if object.check_password(request.POST.get('password')):
                object.first_name = request.POST.get('first_name')
                object.last_name = request.POST.get('last_name')
                object.email = request.POST.get('email')
                object.save()
                return render(request, 'user_info.html', {'error_message': 'Zapisano zmiany!'})
            else:
                return render(request, 'user_edit.html', {'error_message': 'Wprowadzone hasło jest nie poprawne!'})
        except ObjectDoesNotExist:
            return render(request, 'user_edit.html', {'error_message': 'Wprowadzone hasło jest nie poprawne!'})


class UserEditPwd(LoginRequiredMixin, View):
    login_url = '/login/#login'

    def get(self, request):
        return render(request, 'user_change_pwd.html')

    def post(self, request):
        object = SiteUser.objects.get(username=request.user.username)
        if object.check_password(request.POST.get('password')):
            if request.POST.get('password_new') == request.POST.get('password_new2') and len(
                    request.POST.get('password_new')) >= 6:
                object.set_password(request.POST.get('password_new'))
                object.save()
                return render(request, 'user_info.html', {'error_message': 'Zapisano zmiany!'})
            else:
                return render(request, 'user_change_pwd.html', {'error_message': 'Wprowadzone hasła się różnią!'})
        else:
            return render(request, 'user_change_pwd.html', {'error_message': 'Wprowadzone hasło jest nie poprawne!'})


class ContactUs(LoginRequiredMixin, View):
    login_url = '/login/#login'

    def get(self, request):
        return render(request, 'contact_us.html')

    def post(self, request):
        admins = SiteUser.objects.filter(is_staff=True)
        admin_emails = []
        for admin in admins:
            admin_emails.append(admin)
        email_subject = f'Wiadomość od {request.user.email}'
        email_body = render_to_string('contact_us_mail.html',
                                      {'user': request.user.email, 'first_name': request.POST.get('name'),
                                       'last_name': request.POST.get('surname'),
                                       'content': request.POST.get('message')})
        email = EmailMessage(subject=email_subject, body=email_body, from_email=request.user.email,
                             to=admin_emails)
        email.send()
        return render(request, 'index.html', {'error_message': 'Wiadomość została wysłana!'})
