from django.db import models


class Faction(models.Model):

    name = models.CharField(
        "nome",
        max_length=80,
        unique=True,
    )

    slug = models.SlugField(
        max_length=80,
        unique=True,
    )

    code = models.CharField(
        "código",
        max_length=20,
        unique=True,
    )

    symbol = models.CharField(
        "símbolo",
        max_length=20,
        blank=True,
    )

    description = models.TextField(
        "descrição",
    )

    color = models.CharField(
        "cor",
        max_length=7,
        default="#31E6FF",
        help_text="Cor hexadecimal. Ex.: #31E6FF",
    )

    is_active = models.BooleanField(
        "ativa",
        default=True,
    )

    display_order = models.PositiveIntegerField(
        "ordem de exibição",
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = (
            "display_order",
            "name",
        )

        verbose_name = "Factrion"
        verbose_name_plural = "Factrions"

    def __str__(self):
        return self.name