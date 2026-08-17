from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "operador/",
        include(
            "operators.urls"
        ),
    ),

    path(
        "identidade/",
        include(
            "identity.urls"
        ),
    ),

    path(
        "cidade/",
        include(
            "world.urls"
        ),
    ),

    path(
        "",
        include(
            "core.urls"
        ),
    ),
]