from django.shortcuts import redirect


def redirect_operator(operator):

    step = operator.onboarding_step

    if step == operator.OnboardingStep.CHOOSE_FACTION:
        return redirect(
            "identity:choose_faction"
        )

    if step == operator.OnboardingStep.COGNITIVE_TEST:
        return redirect(
            "identity:cognitive_test"
        )

    if step == operator.OnboardingStep.CHOOSE_AVATAR:
        return redirect(
            "identity:choose_avatar"
        )

    if step == operator.OnboardingStep.COMPLETED:
        return redirect(
            "world:city"
        )

    return redirect(
        "core:home"
    )