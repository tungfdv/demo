from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import *


class UserProfileAdmin(BaseUserAdmin):
    """Admin configuration for the UserProfile model."""

    list_display = (
        "user_id",
        "email",
        "username",
        "kana_name",
        "company",
        "role",
        "group",
        "is_active",
        "last_login",
    )
    list_filter = ("is_active", "role", "company", "group")
    fieldsets = (
        ("User Credentials", {"fields": ("user_id", "email", "password")}),
        (
            "Personal info",
            {"fields": ("username", "kana_name", "company", "group", "role", "qrcode")},
        ),
        ("Permissions", {"fields": ("is_active",)}),
        ("Groups", {"fields": ("groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            "Role Management",
            {
                "classes": ("wide",),
                "fields": (
                    "user_id",
                    "email",
                    "username",
                    "kana_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email", "user_id", "username")
    ordering = ("email", "id")


# Register the model with the customized admin
admin.site.register(UserProfile, UserProfileAdmin)
