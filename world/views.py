from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    render,
)

from operators.models import Operator
from operators.services import redirect_operator

from .models import SpawnPoint
from django.conf import settings

from .models import (
    Building,
    CityMap,
    SpawnPoint,
)

@login_required
def city(request):

    operator = request.user

    if (
        operator.onboarding_step
        != Operator.OnboardingStep.COMPLETED
    ):
        return redirect_operator(
            operator
        )


    city_map = get_object_or_404(
        CityMap,
        slug="fortaleza-node",
        is_active=True,
    )


    spawn = (
        SpawnPoint.objects
        .filter(
            map=city_map,
            is_active=True,
            is_default=True,
        )
        .first()
    )


    buildings = (
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


    game_operator = {
        "network_id": operator.network_id,
        "username": operator.username,

        "faction": {
            "name": operator.faction.name,
            "code": operator.faction.code,
        },

        "presentation":
            operator.presentation,

        "shirt_color":
            operator.shirt_color,
    }


    game_buildings = []

    for building in buildings:

        image_url = (
            f"{settings.STATIC_URL}"
            f"{building.image_path}"
        )

        game_buildings.append(
            {
                "id": building.pk,
                "name": building.name,
                "slug": building.slug,

                "image": image_url,

                "x": building.x,
                "y": building.y,

                "width": building.width,
                "height": building.height,

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
            }
        )


    game_world = {
        "id": city_map.pk,
        "name": city_map.name,
        "slug": city_map.slug,

        "width": city_map.width,
        "height": city_map.height,

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

        "buildings":
            game_buildings,
    }


    return render(
        request,
        "world/city.html",
        {
            "game_operator":
                game_operator,

            "game_world":
                game_world,
        },
    )