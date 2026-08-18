import secrets
import string

from django.contrib.auth.models import AbstractUser
from django.db import models


NETWORK_ID_ALPHABET = string.ascii_uppercase + string.digits


def generate_network_id():
    while True:
        code = "".join(
            secrets.choice(NETWORK_ID_ALPHABET)
            for _ in range(6)
        )

        network_id = f"FN-{code}"

        if not Operator.objects.filter(
            network_id=network_id
        ).exists():
            return network_id


class Operator(AbstractUser):

    class OnboardingStep(models.TextChoices):
        CHOOSE_FACTION = (
            "choose_faction",
            "Escolher Facção",
        )

        CHOOSE_AVATAR = (
            "choose_avatar",
            "Escolher aparência",
        )

        COMPLETED = (
            "completed",
            "Concluído",
        )

    class Presentation(models.TextChoices):
        MALE = (
            "male",
            "Masculino",
        )

        FEMALE = (
            "female",
            "Feminino",
        )


    class ShirtColor(models.TextChoices):
        CYAN = (
            "cyan",
            "Ciano",
        )

        PURPLE = (
            "purple",
            "Roxo",
        )

        GREEN = (
            "green",
            "Verde",
        )

        RED = (
            "red",
            "Vermelho",
        )

        YELLOW = (
            "yellow",
            "Amarelo",
        )

        WHITE = (
            "white",
            "Branco",
        )

    email = models.EmailField(
        "e-mail",
        unique=True,
    )

    network_id = models.CharField(
        "Registro FN",
        max_length=9,
        unique=True,
        editable=False,
        blank=True,
    )

    faction = models.ForeignKey(
        "identity.Faction",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="operators",
        verbose_name="Factrion",
    )

    presentation = models.CharField(
        "apresentação",
        max_length=10,
        choices=Presentation.choices,
        blank=True,
    )

    shirt_color = models.CharField(
        "cor da camiseta",
        max_length=20,
        choices=ShirtColor.choices,
        blank=True,
    )


    onboarding_step = models.CharField(
        max_length=30,
        choices=OnboardingStep.choices,
        default=OnboardingStep.CHOOSE_FACTION,
    )

    onboarding_completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):
        if not self.network_id:
            self.network_id = generate_network_id()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} [{self.network_id}]"