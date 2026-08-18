from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import AvatarSelectionForm

from operators.models import Operator
from operators.services import redirect_operator

from .models import Faction


@login_required
def choose_faction(request):

    if (
        request.user.onboarding_step
        != Operator.OnboardingStep.CHOOSE_FACTION
    ):
        return redirect_operator(
            request.user
        )

    if request.user.faction_id:
        return redirect_operator(
            request.user
        )

    factions = Faction.objects.filter(
        is_active=True
    )

    return render(
        request,
        "identity/choose_faction.html",
        {
            "factions": factions,
        },
    )


@login_required
def confirm_faction(request, faction_slug):

    if (
        request.user.onboarding_step
        != Operator.OnboardingStep.CHOOSE_FACTION
    ):
        return redirect_operator(
            request.user
        )

    if request.user.faction_id:
        return redirect_operator(
            request.user
        )

    faction = get_object_or_404(
        Faction,
        slug=faction_slug,
        is_active=True,
    )

    if request.method == "POST":

        with transaction.atomic():

            operator = (
                Operator.objects
                .select_for_update()
                .get(pk=request.user.pk)
            )

            if (
                operator.onboarding_step
                != Operator.OnboardingStep.CHOOSE_FACTION
                or operator.faction_id
            ):
                return redirect_operator(
                    operator
                )

            operator.faction = faction

            operator.onboarding_step = (
                Operator.OnboardingStep.CHOOSE_AVATAR
            )

            operator.save(
                update_fields=[
                    "faction",
                    "onboarding_step",
                    "updated_at",
                ]
            )

        return redirect(
            "identity:choose_avatar"
        )

    return render(
        request,
        "identity/confirm_faction.html",
        {
            "faction": faction,
        },
    )


@login_required
def cognitive_test(request):

    return render(
        request,
        "identity/cognitive_test.html",
    )


@login_required
def choose_avatar(request):

    if (
        request.user.onboarding_step
        != Operator.OnboardingStep.CHOOSE_AVATAR
    ):
        return redirect_operator(
            request.user
        )

    if request.method == "POST":

        form = AvatarSelectionForm(
            request.POST
        )

        if form.is_valid():

            operator = request.user

            operator.presentation = (
                form.cleaned_data["presentation"]
            )

            operator.shirt_color = (
                form.cleaned_data["shirt_color"]
            )

            operator.onboarding_step = (
                Operator.OnboardingStep.COMPLETED
            )

            operator.onboarding_completed_at = (
                timezone.now()
            )

            operator.save(
                update_fields=[
                    "presentation",
                    "shirt_color",
                    "onboarding_step",
                    "onboarding_completed_at",
                    "updated_at",
                ]
            )

            return redirect(
                "world:city"
            )

    else:

        form = AvatarSelectionForm()

    return render(
        request,
        "identity/choose_avatar.html",
        {
            "form": form,
        },
    )