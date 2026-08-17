from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Operator


@admin.register(Operator)
class OperatorAdmin(UserAdmin):
    pass