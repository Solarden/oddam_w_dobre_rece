"""oddam_w_dobre_rece URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LandingPage.as_view(), name='landing_page'),
    path('add_donation/', views.AddDonation.as_view(), name='add_donation'),
    path('register/', views.Register.as_view(), name='register'),
    path('activate_user/<uidb64>/<token>', views.ActivateUser.as_view(), name='activate'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user/', views.UserInfo.as_view(), name='user'),
    path('user/edit/', views.UserEdit.as_view(), name='user_edit'),
    path('user/edit/password/', views.UserEditPwd.as_view(), name='user_edit_pwd'),
    path('user/reset_password/', auth_views.PasswordResetView.as_view(template_name='user_reset_password.html'),
         name='reset_password'),
    path('user/reset_password/sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='user_reset_password_sent.html'),
         name='password_reset_done'),
    path('user/reset_password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user_reset_password_form.html'),
         name='password_reset_confirm'),
    path('user/reset_password/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user_reset_password_done.html'),
         name='password_reset_complete'),
    path('contact_us/', views.ContactUs.as_view(), name='contact_us'),
]
