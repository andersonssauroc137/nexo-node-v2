from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from operators.models import Operator
from operators.services import redirect_operator


@login_required
def choose_faction(request):

    if (
        request.user.onboarding_step
        != Operator.OnboardingStep.CHOOSE_FACTION
    ):
        return redirect_operator(
            request.user
        )

    return render(
        request,
        "identity/choose_faction.html",
    )


@login_required
def cognitive_test(request):

    if (
        request.user.onboarding_step
        != Operator.OnboardingStep.COGNITIVE_TEST
    ):
        return redirect_operator(
            request.user
        )

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

    return render(
        request,
        "identity/choose_avatar.html",
    )