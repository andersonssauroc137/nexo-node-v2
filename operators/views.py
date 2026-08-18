from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import OperatorRegistrationForm
from .services import redirect_operator



def register(request):

    if request.user.is_authenticated:
        return redirect_operator(
            request.user
        )

    if request.method == "POST":
        form = OperatorRegistrationForm(
            request.POST
        )

        if form.is_valid():
            operator = form.save()

            login(
                request,
                operator,
            )

            return redirect_operator(
                operator
            )

    else:
        form = OperatorRegistrationForm()

    return render(
        request,
        "operators/register.html",
        {
            "form": form,
        },
    )


class OperatorLoginView(LoginView):

    template_name = "operators/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        operator = self.request.user

        step = operator.onboarding_step

        if (
            step
            == operator.OnboardingStep.CHOOSE_FACTION
        ):
            return reverse(
                "identity:choose_faction"
            )

        if (
            step
            == operator.OnboardingStep.CHOOSE_AVATAR
        ):
            return reverse(
                "identity:choose_avatar"
            )

        return reverse(
            "world:city"
        )

@login_required
def continue_onboarding(request):
    return redirect_operator(
        request.user
    )