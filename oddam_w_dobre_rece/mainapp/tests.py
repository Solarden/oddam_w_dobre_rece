import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client
from django.urls import reverse


# Create your tests here.

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


# TODO add_donation_post

@pytest.mark.django_db
def test_login():
    client = Client()
    response = client.get(reverse('login'))
    assert response.status_code == 200


# TODO login post

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


# TODO register post

@pytest.mark.django_db
def test_activate_user():
    client = Client()
    response = client.get(reverse('register'))
    assert response.status_code == 200
