from django import forms

from operators.models import Operator


class AvatarSelectionForm(forms.Form):

    presentation = forms.ChoiceField(
        label="Apresentação",
        choices=Operator.Presentation.choices,
        widget=forms.RadioSelect,
    )

    shirt_color = forms.ChoiceField(
        label="Cor da camiseta",
        choices=Operator.ShirtColor.choices,
        widget=forms.RadioSelect,
    )