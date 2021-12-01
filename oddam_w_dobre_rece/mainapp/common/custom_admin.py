from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")

    def has_delete_permission(self, request, obj=None):
        return False
