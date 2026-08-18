from django.test import TestCase
from django.urls import reverse

from operators.models import Operator
from .models import SpawnPoint

from identity.models import Faction


class CityAccessTests(TestCase):

    def setUp(self):
        self.faction = Faction.objects.create(
            name="Cangaceiros Digitais",
            slug="cangaceiros-digitais",
            code="CD",
            symbol="CD",
            description="Factrion de teste.",
            color="#FF8A5B",
            display_order=10,
        )

        self.operator = (
            Operator.objects.create_user(
                username="sentinela7",
                email="s7@nexo.test",
                password="StrongTestPass989!",
            )
        )

        self.client.force_login(
            self.operator
        )

    def test_incomplete_operator_cannot_access_city(
        self
    ):

        response = self.client.get(
            reverse(
                "world:city"
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "identity:choose_faction"
            ),
        )

def test_completed_operator_can_access_city(
    self
):

    self.operator.faction = (
        self.faction
    )

    self.operator.presentation = (
        Operator.Presentation.MALE
    )

    self.operator.shirt_color = (
        Operator.ShirtColor.CYAN
    )

    self.operator.onboarding_step = (
        Operator.OnboardingStep.COMPLETED
    )

    self.operator.save()

    response = self.client.get(
        reverse(
            "world:city"
        )
    )

    self.assertEqual(
        response.status_code,
        200,
    )

def test_city_receives_game_data(
    self
):

    self.operator.faction = (
        self.faction
    )

    self.operator.presentation = (
        Operator.Presentation.MALE
    )

    self.operator.shirt_color = (
        Operator.ShirtColor.GREEN
    )

    self.operator.onboarding_step = (
        Operator.OnboardingStep.COMPLETED
    )

    self.operator.save()

    SpawnPoint.objects.create(
        name="Entrada Inicial",
        code="initial-entry",
        x=1600,
        y=1100,
        is_default=True,
    )

    response = self.client.get(
        reverse(
            "world:city"
        )
    )

    self.assertEqual(
        response.status_code,
        200,
    )

    self.assertEqual(
        response.context[
            "game_operator"
        ]["network_id"],
        self.operator.network_id,
    )

    self.assertEqual(
        response.context[
            "game_world"
        ]["spawn"]["x"],
        1600,
    )

    self.assertEqual(
        response.context[
            "game_world"
        ]["spawn"]["y"],
        1100,
    )
class SpawnPointTests(TestCase):

    def test_only_one_spawn_is_default(
        self
    ):

        first = (
            SpawnPoint.objects.create(
                name="Entrada A",
                code="entrada-a",
                x=100,
                y=100,
                is_default=True,
            )
        )


        second = (
            SpawnPoint.objects.create(
                name="Entrada B",
                code="entrada-b",
                x=200,
                y=200,
                is_default=True,
            )
        )


        first.refresh_from_db()
        second.refresh_from_db()


        self.assertFalse(
            first.is_default
        )

        self.assertTrue(
            second.is_default
        )