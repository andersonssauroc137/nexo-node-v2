from django.test import TestCase
from django.urls import reverse

from identity.models import Faction
from operators.models import Operator

from .models import (
    Building,
    CityMap,
    SpawnPoint,
)


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

        self.city_map = CityMap.objects.create(
            name="Fortaleza Node",
            slug="fortaleza-node",
            width=3200,
            height=2200,
        )

        self.operator = Operator.objects.create_user(
            username="sentinela7",
            email="s7@nexo.test",
            password="StrongTestPass989!",
        )

        self.client.force_login(
            self.operator
        )

    def complete_operator(self):

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

        self.complete_operator()

        response = self.client.get(
            reverse(
                "world:city"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_city_receives_buildings(
        self
    ):

        self.complete_operator()

        SpawnPoint.objects.create(
            map=self.city_map,
            name="Entrada Inicial",
            code="initial-entry",
            x=1600,
            y=1100,
            is_default=True,
        )

        Building.objects.create(
            map=self.city_map,
            name="Bloco 01",
            slug="bloco-01",
            image_path=(
                "world/img/buildings/"
                "building_01.png"
            ),
            x=900,
            y=500,
            width=320,
            height=320,
            collision_offset_x=30,
            collision_offset_y=210,
            collision_width=260,
            collision_height=100,
        )

        response = self.client.get(
            reverse(
                "world:city"
            )
        )

        buildings = (
            response.context[
                "game_world"
            ]["buildings"]
        )

        self.assertEqual(
            len(buildings),
            1,
        )

        self.assertEqual(
            buildings[0]["slug"],
            "bloco-01",
        )

        self.assertEqual(
            buildings[0]["collision"]["x"],
            930,
        )

        self.assertEqual(
            buildings[0]["collision"]["y"],
            710,
        )

    def test_inactive_building_is_not_sent_to_game(
        self
    ):

        self.complete_operator()

        Building.objects.create(
            map=self.city_map,
            name="Bloco Inativo",
            slug="bloco-inativo",
            image_path=(
                "world/img/buildings/"
                "inactive.png"
            ),
            x=100,
            y=100,
            width=100,
            height=100,
            collision_width=80,
            collision_height=40,
            is_active=False,
        )

        response = self.client.get(
            reverse(
                "world:city"
            )
        )

        buildings = (
            response.context[
                "game_world"
            ]["buildings"]
        )

        self.assertEqual(
            len(buildings),
            0,
        )

    def test_city_receives_game_data(
        self
    ):

        self.complete_operator()

        SpawnPoint.objects.create(
            map=self.city_map,
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

        first = SpawnPoint.objects.create(
            name="Entrada A",
            code="entrada-a",
            x=100,
            y=100,
            is_default=True,
        )

        second = SpawnPoint.objects.create(
            name="Entrada B",
            code="entrada-b",
            x=200,
            y=200,
            is_default=True,
        )

        first.refresh_from_db()
        second.refresh_from_db()

        self.assertFalse(
            first.is_default
        )

        self.assertTrue(
            second.is_default
        )


class BuildingTests(TestCase):

    def setUp(self):

        self.city_map = CityMap.objects.create(
            name="Fortaleza Node",
            slug="fortaleza-node",
            width=3200,
            height=2200,
        )

    def test_collision_position_uses_offsets(
        self
    ):

        building = Building.objects.create(
            map=self.city_map,
            name="Bloco 01",
            slug="bloco-01",
            image_path=(
                "world/img/buildings/"
                "building_01.png"
            ),
            x=900,
            y=500,
            width=320,
            height=320,
            collision_offset_x=30,
            collision_offset_y=210,
            collision_width=260,
            collision_height=100,
        )

        self.assertEqual(
            building.collision_x,
            930,
        )

        self.assertEqual(
            building.collision_y,
            710,
        )