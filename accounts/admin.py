from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (_("Personal info"), {"fields": ("email", "password")}),
        (_("Permissions"), {
            "fields": (
                "is_superuser", "is_staff", "is_active",
                "groups", "user_permissions"
                )
            }
         ),
        (_("Important dates"), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ["email"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user", "first_name", "last_name",
        "gender", "created_at", "updated_at"
    ]
    search_fields = ["user", "first_name", "last_name"]
    list_filter = ["gender", "created_at", "updated_at"]

