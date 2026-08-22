from django.urls import path

from . import views


app_name = "world"


urlpatterns = [

    path(
        "",
        views.city,
        name="city",
    ),

    path(
        "mapa/<slug:map_slug>/",
        views.map_view,
        name="map",
    ),

]