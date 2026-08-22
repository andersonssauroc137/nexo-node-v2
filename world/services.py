from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import (
    Building,
    CityMap,
    SpawnPoint,
)


def get_active_map(
    map_slug,
):

    return get_object_or_404(
        CityMap,
        slug=map_slug,
        is_active=True,
    )


def get_default_spawn(
    city_map,
):

    return (
        SpawnPoint.objects
        .filter(
            map=city_map,
            is_active=True,
            is_default=True,
        )
        .first()
    )


def get_active_buildings(
    city_map,
):

    return (
        Building.objects
        .filter(
            map=city_map,
            is_active=True,
        )
        .order_by(
            "display_order",
            "name",
        )
    )


def serialize_building(
    building,
):

    image_url = (
        f"{settings.STATIC_URL}"
        f"{building.image_path}"
    )

    return {
        "id":
            building.pk,

        "name":
            building.name,

        "slug":
            building.slug,

        "image":
            image_url,

        "x":
            building.x,

        "y":
            building.y,

        "width":
            building.width,

        "height":
            building.height,

        "collision": {
            "x":
                building.collision_x,

            "y":
                building.collision_y,

            "width":
                building.collision_width,

            "height":
                building.collision_height,
        },

        "interaction": {
            "enabled":
                building.has_entrance,

            "x":
                building.interaction_x,

            "y":
                building.interaction_y,

            "width":
                building.interaction_width,

            "height":
                building.interaction_height,

            "type":
                "entrance",
        },
    }


def build_map_data(
    city_map,
):

    spawn = get_default_spawn(
        city_map
    )

    buildings = (
        get_active_buildings(
            city_map
        )
    )

    return {
        "id":
            city_map.pk,

        "name":
            city_map.name,

        "slug":
            city_map.slug,

        "width":
            city_map.width,

        "height":
            city_map.height,

        "spawn": {
            "x":
                spawn.x
                if spawn
                else city_map.width // 2,

            "y":
                spawn.y
                if spawn
                else city_map.height // 2,
        },

        "buildings": [
            serialize_building(
                building
            )
            for building in buildings
        ],
    }
    
def build_operator_data(
    operator,
):

    return {
        "network_id":
            operator.network_id,

        "username":
            operator.username,

        "faction": {
            "name":
                operator.faction.name,

            "code":
                operator.faction.code,
        },

        "presentation":
            operator.presentation,

        "shirt_color":
            operator.shirt_color,
    }