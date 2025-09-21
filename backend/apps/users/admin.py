from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Role, User


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (("Roles", {"fields": ("roles",)}),)
    filter_horizontal = DjangoUserAdmin.filter_horizontal + ("roles",)

    list_display = DjangoUserAdmin.list_display + ("display_primary_role",)

    @admin.display(description="Primary role")
    def display_primary_role(self, obj):
        return obj.primary_role or "-"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("roles")
