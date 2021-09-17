from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm
from users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "User Details",
            {
                "fields": (
                    "gender",
                    "income_group",
                    "region",
                    "marital_status",
                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)