import pytest
from .models import SiteUser, Institution, Category
from django.contrib.auth.models import Permission, Group


@pytest.fixture
def site_user():
    return SiteUser.objects.create(username='testowyj')


@pytest.fixture
def site_user_pwd():
    user = SiteUser.objects.create(username='testowy', email='test@test.pl')
    user.set_password('Tymczasowe1!')
    return user

@pytest.fixture
def add_category():
    return Category.objects.create(name='test')


@pytest.fixture
def add_institution(add_category):
    a = Institution.objects.create(name='testowa', description='test', city_location='test')
    a.categories.set(add_category)
    a.save()
    return a
