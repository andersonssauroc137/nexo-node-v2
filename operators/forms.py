from django import forms
from django.contrib.auth.forms import BaseUserCreationForm

from .models import Operator


class OperatorRegistrationForm(BaseUserCreationForm):

    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "operador@rede.com",
                "autocomplete": "email",
            }
        ),
    )

    class Meta:
        model = Operator
        fields = (
            "username",
            "email",
        )

    def clean_email(self):
        email = self.cleaned_data[
            "email"
        ].strip().lower()

        if Operator.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "Este e-mail já está vinculado "
                "a um Operador."
            )

        return email