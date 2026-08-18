from django.contrib import admin

from .models import SpawnPoint


@admin.register(SpawnPoint)
class SpawnPointAdmin(
    admin.ModelAdmin
):

    list_display = (
        "name",
        "code",
        "x",
        "y",
        "is_default",
        "is_active",
    )

    list_filter = (
        "is_default",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )