from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {"fields": ("role", "is_staff", "is_active")},
        ),
        (
            "Dates",
            {"fields": ("last_login",)},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role"),
            },
        ),
    )

    list_display = ("email", "role", "is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = (
        "user",
        "city",
        "phone",
    )