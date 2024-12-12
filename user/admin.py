from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    """Admin configuration for the CustomUser model."""

    list_display = (
        "email",
        "username",
        "is_active",
        "last_login",
    )

    list_filter = ("is_active",)

    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active",)}),
        ("Groups", {"fields": ("groups", "user_permissions")}),
    )

    add_fieldsets = (
        (
            "Role Management",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email", "username")
    ordering = ("email", "id")


admin.site.register(CustomUser, CustomUserAdmin)
