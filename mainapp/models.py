from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.

class SiteUser(AbstractUser):
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    INSTITUTION_TYPES = {
        (0, 'Fundacja'),
        (1, 'Organizacja pozarządowa'),
        (2, 'Zbiórka lokalna'),
    }

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    type = models.IntegerField(choices=INSTITUTION_TYPES, default=0)
    categories = models.ManyToManyField(Category)
    city_location = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    address = models.TextField()
    phone_no = models.CharField(max_length=9)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(SiteUser, null=True, on_delete=models.PROTECT)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.pick_up_date}'

