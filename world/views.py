from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from operators.models import Operator
from operators.services import redirect_operator


@login_required
def city(request):

    if (
        request.user.onboarding_step
        != Operator.OnboardingStep.COMPLETED
    ):
        return redirect_operator(
            request.user
        )

    return render(
        request,
        "world/city.html",
    )