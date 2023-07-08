from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser, Ban


def ban_users(admin, request, queryset):
    queryset.update(is_banned=False)
    for user in queryset:
        Ban.objects.create(user=user, reason="Banned for violating terms of service")


def unban_users(admin, request, queryset):
    queryset.update(is_banned=True)
    for user in queryset:
        Ban.objects.filter(user=user).delete()


class CustomUserAdmin(UserAdmin):
    form = CustomUserUpdateForm
    actions = [ban_users, unban_users]
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("User Information", {"fields": ("email",)}),
        ("Personal Information", {"fields": ("profile_picture",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_banned",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    list_display = ("id", "username", "email", "is_staff", "is_banned")
    list_filter = ("is_staff", "is_active", "is_banned")
    filter_horizontal = ()
    ordering = ("username",)


admin.site.register(CustomUser, CustomUserAdmin)
