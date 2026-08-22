from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from operators.models import Operator
from operators.services import redirect_operator

from .services import (
    build_map_data,
    build_operator_data,
    get_active_map,
)


MAIN_CITY_SLUG = "fortaleza-node"


def _render_map(
    request,
    map_slug,
):

    city_map = get_active_map(
        map_slug
    )

    game_operator = (
        build_operator_data(
            request.user
        )
    )

    game_world = (
        build_map_data(
            city_map
        )
    )

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

    return _render_map(
        request,
        MAIN_CITY_SLUG,
    )


@login_required
def map_view(
    request,
    map_slug,
):

    operator = request.user

    if (
        operator.onboarding_step
        != Operator.OnboardingStep.COMPLETED
    ):
        return redirect_operator(
            operator
        )

    return _render_map(
        request,
        map_slug,
    )