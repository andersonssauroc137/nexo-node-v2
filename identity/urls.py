from django.urls import path

from . import views


app_name = "identity"


urlpatterns = [

    path(
        "faccao/",
        views.choose_faction,
        name="choose_faction",
    ),

    path(
        "faccao/<slug:faction_slug>/",
        views.confirm_faction,
        name="confirm_faction",
    ),

    path(
        "teste/",
        views.cognitive_test,
        name="cognitive_test",
    ),

    path(
        "avatar/",
        views.choose_avatar,
        name="choose_avatar",
    ),
]