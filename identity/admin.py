from django.contrib import admin

from .models import Faction


@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "is_active",
        "display_order",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "slug",
    )

    ordering = (
        "display_order",
        "name",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        )
    }