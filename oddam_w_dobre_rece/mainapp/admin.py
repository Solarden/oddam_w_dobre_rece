from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from mainapp import models
from django.db import models as db_models


class BaseAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        admins = models.SiteUser.objects.filter(is_staff=True)
        if len(admins) > 1:
            return True
        else:
            return False


class DummyModel(db_models.Model):
    class Meta:
        verbose_name_plural = 'Lista administratorów'
        app_label = 'mainapp'


def my_custom_view(request):
    return HttpResponse('test')


class DummyModelAdmin(admin.ModelAdmin):
    model = DummyModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name)
        return [path('admin/', my_custom_view, name=view_name)]


admin.site.register(DummyModel, DummyModelAdmin)
admin.site.register(models.Donation)
admin.site.register(models.Category)
admin.site.register(models.Institution)
admin.site.register(models.SiteUser, BaseAdmin)
