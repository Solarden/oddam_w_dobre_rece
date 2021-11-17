from django.contrib import admin
from mainapp import models
# Register your models here.

admin.site.register(models.Donation)
admin.site.register(models.Category)
admin.site.register(models.Institution)
