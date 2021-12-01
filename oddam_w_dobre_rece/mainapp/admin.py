from django.contrib import admin
from mainapp import models


class BaseAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        admins = models.SiteUser.objects.filter(is_staff=True)
        if len(admins) > 1:
            return True
        else:
            return False


admin.site.register(models.Donation)
admin.site.register(models.Category)
admin.site.register(models.Institution)
admin.site.register(models.SiteUser, BaseAdmin)
