from django.db import models


class SpawnPoint(models.Model):

    name = models.CharField(
        "nome",
        max_length=80,
    )

    code = models.SlugField(
        "código",
        max_length=80,
        unique=True,
    )

    x = models.PositiveIntegerField()

    y = models.PositiveIntegerField()

    is_default = models.BooleanField(
        "spawn padrão",
        default=False,
    )

    is_active = models.BooleanField(
        "ativo",
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:
        ordering = (
            "name",
        )

        verbose_name = (
            "Ponto de Spawn"
        )

        verbose_name_plural = (
            "Pontos de Spawn"
        )


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.is_default:

            SpawnPoint.objects.filter(
                is_default=True
            ).exclude(
                pk=self.pk
            ).update(
                is_default=False
            )

        super().save(
            *args,
            **kwargs
        )