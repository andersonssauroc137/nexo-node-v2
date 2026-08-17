from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    OperatorLoginView,
    continue_onboarding,
    register,
)


app_name = "operators"


urlpatterns = [

    path(
        "cadastro/",
        register,
        name="register",
    ),

    path(
        "continuar/",
        continue_onboarding,
        name="continue",
    ),

    path(
        "entrar/",
        OperatorLoginView.as_view(),
        name="login",
    ),

    path(
        "sair/",
        LogoutView.as_view(),
        name="logout",
    ),
]