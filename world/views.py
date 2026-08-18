from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from operators.models import Operator
from operators.services import redirect_operator

from .models import SpawnPoint


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


    game_operator = {
        "network_id": operator.network_id,
        "username": operator.username,
        "faction": {
            "name": operator.faction.name,
            "code": operator.faction.code,
        },
        "presentation": operator.presentation,
        "shirt_color": operator.shirt_color,
    }

    spawn = (
        SpawnPoint.objects
        .filter(
            is_active=True,
            is_default=True,
        )
        .first()
    )

    game_world = {
        "width": 3200,
        "height": 2200,
        "spawn": {
            "x": spawn.x if spawn else 1600,
            "y": spawn.y if spawn else 1100,
        },
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