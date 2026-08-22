from django.db import models

class CityMap(models.Model):

    name = models.CharField(
        "nome",
        max_length=100,
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    width = models.PositiveIntegerField(
        "largura",
        default=3200,
    )

    height = models.PositiveIntegerField(
        "altura",
        default=2200,
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
        verbose_name = "Mapa"
        verbose_name_plural = "Mapas"

    def __str__(self):
        return self.name

class SpawnPoint(models.Model):

    name = models.CharField(
        "nome",
        max_length=80,
    )

    map = models.ForeignKey(
        CityMap,
        on_delete=models.CASCADE,
        related_name="spawn_points",
        verbose_name="mapa",
        null=True,
        blank=True,
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
                map=self.map,
                is_default=True,
            ).exclude(
                pk=self.pk
            ).update(
                is_default=False
            )

        super().save(
            *args,
            **kwargs
        )

class Building(models.Model):

    map = models.ForeignKey(
        CityMap,
        on_delete=models.CASCADE,
        related_name="buildings",
        verbose_name="mapa",
    )

    name = models.CharField(
        "nome",
        max_length=120,
    )

    slug = models.SlugField(
        max_length=120,
    )

    image_path = models.CharField(
        "caminho da imagem",
        max_length=255,
        help_text=(
            "Ex.: world/img/buildings/building_01.png"
        ),
    )

    x = models.IntegerField(
        "posição X",
    )

    y = models.IntegerField(
        "posição Y",
    )

    width = models.PositiveIntegerField(
        "largura visual",
    )

    height = models.PositiveIntegerField(
        "altura visual",
    )

    collision_offset_x = models.IntegerField(
        "offset colisão X",
        default=0,
    )

    collision_offset_y = models.IntegerField(
        "offset colisão Y",
        default=0,
    )

    collision_width = models.PositiveIntegerField(
        "largura da colisão",
    )

    collision_height = models.PositiveIntegerField(
        "altura da colisão",
    )

    is_active = models.BooleanField(
        "ativo",
        default=True,
    )

    display_order = models.PositiveIntegerField(
        "ordem",
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    interaction_offset_x = models.IntegerField(
    "offset interação X",
    default=0,
    )

    interaction_offset_y = models.IntegerField(
        "offset interação Y",
        default=0,
    )

    interaction_width = models.PositiveIntegerField(
        "largura da interação",
        default=48,
    )

    interaction_height = models.PositiveIntegerField(
        "altura da interação",
        default=32,
    )

    has_entrance = models.BooleanField(
        "possui entrada",
        default=False,
    )
    
    @property
    def interaction_x(self):
        return (
            self.x
            + self.interaction_offset_x
        )


    @property
    def interaction_y(self):
        return (
            self.y
            + self.interaction_offset_y
        )

        class Meta:
            ordering = (
                "display_order",
                "name",
            )

            constraints = [
                models.UniqueConstraint(
                    fields=(
                        "map",
                        "slug",
                    ),
                    name="unique_building_slug_per_map",
                ),
            ]

            verbose_name = "Prédio"
            verbose_name_plural = "Prédios"

    @property
    def collision_x(self):
        return (
            self.x
            + self.collision_offset_x
        )

    @property
    def collision_y(self):
        return (
            self.y
            + self.collision_offset_y
        )

    def __str__(self):
        return (
            f"{self.name} — "
            f"{self.map.name}"
        )