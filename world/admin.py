from django.contrib import admin

from .models import (
    Building,
    CityMap,
    SpawnPoint,
)

@admin.register(SpawnPoint)
class SpawnPointAdmin(
    admin.ModelAdmin
):

    list_display = (
        "name",
        "map",
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

@admin.register(CityMap)
class CityMapAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "width",
        "height",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "slug",
    )

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "map",
        "x",
        "y",
        "width",
        "height",
        "is_active",
    )

    list_filter = (
        "map",
        "is_active",
    )

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        )
    }

    fieldsets = (
        (
            "Identificação",
            {
                "fields": (
                    "map",
                    "name",
                    "slug",
                    "image_path",
                    "is_active",
                    "display_order",
                )
            },
        ),
        (
            "Visual",
            {
                "fields": (
                    "x",
                    "y",
                    "width",
                    "height",
                )
            },
        ),
        (
            "Colisão",
            {
                "fields": (
                    "collision_offset_x",
                    "collision_offset_y",
                    "collision_width",
                    "collision_height",
                )
            },
        ),
        (
            "Interação",
            {
                "fields": (
                    "has_entrance",
                    "interaction_offset_x",
                    "interaction_offset_y",
                    "interaction_width",
                    "interaction_height",
                )
            },
        ),
    )