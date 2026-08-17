from django.core.management.base import BaseCommand

from identity.models import Faction


FACTIONS = [
    {
        "name": "Polícia da Rede",
        "slug": "policia-da-rede",
        "code": "PR",
        "symbol": "PR",
        "description": (
            "Defende estabilidade, rastreabilidade "
            "e ordem dentro da infraestrutura da Rede."
        ),
        "color": "#31E6FF",
        "display_order": 10,
    },
    {
        "name": "Terra Nova",
        "slug": "terra-nova",
        "code": "TN",
        "symbol": "TN",
        "description": (
            "Acredita na transformação tecnológica "
            "como ferramenta para reconstruir estruturas "
            "sociais e urbanas."
        ),
        "color": "#55E39F",
        "display_order": 20,
    },
    {
        "name": "Mascarados",
        "slug": "mascarados",
        "code": "MSK",
        "symbol": "M",
        "description": (
            "Valoriza anonimato, autonomia e identidades "
            "que não dependem das estruturas tradicionais "
            "da Rede."
        ),
        "color": "#A96BFF",
        "display_order": 30,
    },
    {
        "name": "Beatos",
        "slug": "beatos",
        "code": "BT",
        "symbol": "B",
        "description": (
            "Interpreta tecnologia, conhecimento e memória "
            "como partes de uma tradição que precisa ser "
            "preservada."
        ),
        "color": "#FFD76A",
        "display_order": 40,
    },
    {
        "name": "Cangaceiros Digitais",
        "slug": "cangaceiros-digitais",
        "code": "CD",
        "symbol": "CD",
        "description": (
            "Opera nas margens das estruturas formais, "
            "valorizando independência, improvisação "
            "e resistência."
        ),
        "color": "#FF8A5B",
        "display_order": 50,
    },
    {
        "name": "Caçadores",
        "slug": "cacadores",
        "code": "CCT",
        "symbol": "C",
        "description": (
            "Busca sinais, rastros, informações e fenômenos "
            "que outros Operadores normalmente ignoram."
        ),
        "color": "#FF657A",
        "display_order": 60,
    },
    {
        "name": "Mercadores",
        "slug": "mercadores",
        "code": "MRC",
        "symbol": "M",
        "description": (
            "Enxerga circulação de recursos, serviços "
            "e informação como o verdadeiro sistema "
            "nervoso de Fortaleza Node."
        ),
        "color": "#5BBEFF",
        "display_order": 70,
    },
]


class Command(BaseCommand):

    help = "Cria ou atualiza as Factrions iniciais."

    def handle(self, *args, **options):

        for data in FACTIONS:

            faction, created = (
                Faction.objects.update_or_create(
                    code=data["code"],
                    defaults=data,
                )
            )

            action = (
                "criada"
                if created
                else "atualizada"
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"{faction.name}: {action}"
                )
            )
