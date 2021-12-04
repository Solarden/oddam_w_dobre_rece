import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client
from django.urls import reverse

# Create your tests here.
from mainapp.models import SiteUser


@pytest.mark.django_db
def test_landing_page():
    client = Client()
    response = client.get(reverse("landing_page"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_donation_no_login():
    client = Client()
    response = client.get(reverse('add_donation'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_donation_with_login(site_user):
    client = Client()
    client.force_login(site_user)
    response = client.get(reverse('add_donation'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_donation_with_login_post(add_institution, site_user):
    client = Client()
    a = {
        'quantity': '3',
        'institution': add_institution,
        'address': 'test',
        'phone_no': '123',
        'city': 'test',
        'zip_code': '12',
        'pick_up_date': '2021-01-01',
        'pick_up_time': '12:12',
        'pick_up_comment': 'test',
        'user': site_user,
    }
    response = client.post(reverse("add_donation"), data=a)
    assert response.status_code == 302
    SiteUser.objects.get(**a)


@pytest.mark.django_db
def test_login():
    client = Client()
    response = client.get(reverse('login'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_post(site_user_pwd):
    client = Client()
    b = {
        'email': 'test@test.pl',
        'password': 'Tymczasowe1!',
    }
    response = client.post(reverse("login"), data=b)
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_no_login():
    client = Client()
    response = client.get(reverse('logout'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_with_login(site_user):
    client = Client()
    client.force_login(site_user)
    response = client.get(reverse('logout'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_register():
    client = Client()
    response = client.get(reverse('register'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_post():
    client = Client()
    a = {
        'name': 'test',
        'surname': 'testowy',
        'email': 'test@test.pl',
        'password': 'Tymczasowe1!',
        'password2': 'Tymczasowe1!',
    }
    response = client.post(reverse("register"), data=a)
    assert response.status_code == 302


@pytest.mark.django_db
def test_activate_user():
    client = Client()
    response = client.get(reverse('register'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_info_no_login():
    client = Client()
    response = client.get(reverse('user'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_info_with_login(site_user):
    client = Client()
    client.force_login(site_user)
    response = client.get(reverse('user'))
    assert response.status_code == 302
