import pytest
from .models import SiteUser
from django.contrib.auth.models import Permission, Group


@pytest.fixture
def site_user():
    return SiteUser.objects.create(username='testowy')
