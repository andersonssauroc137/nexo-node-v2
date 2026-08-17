from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Operator


@admin.register(Operator)
class OperatorAdmin(UserAdmin):

    list_display = (
        "username",
        "network_id",
        "email",
        "faction",
        "onboarding_step",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "network_id",
    )

    readonly_fields = (
        "network_id",
        "last_login",
        "date_joined",
        "updated_at",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "NEXO NODE",
            {
                "fields": (
                    "network_id",
                    "faction",
                    "onboarding_step",
                    "onboarding_completed_at",
                    "updated_at",
                )
            },
        ),
    )