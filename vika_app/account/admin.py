from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from vika_app.account.models import User


class AccountAdmin(UserAdmin):

    list_display = ("__str__", "phone", "user_type", "date_joined", "is_staff")
    ordering = (
        "pk",
        "is_staff",
    )
    search_fields = ("phone",)
    list_per_page = 150

    profile_fieldsets = (
        (
            "Права",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "user_type",
                    "groups",
                )
            },
        ),
        (
            "Персональная информация",
            {
                "fields": (
                    "name",
                    "phone",
                    "age",
                    "gender",
                ),
            },
        ),
    )

    fieldsets = ((None, {"fields": ("password",)}), *profile_fieldsets)

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "user_type",
                    "password1",
                    "password2",
                )
            },
        ),
    )


admin.site.register(User, AccountAdmin)
