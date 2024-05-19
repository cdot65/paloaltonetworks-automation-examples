from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "name", "is_staff"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name", "profile_image")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("name", "profile_image")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
