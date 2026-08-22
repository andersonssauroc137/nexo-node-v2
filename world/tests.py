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

    def setUp(self):

        self.city_map = (
            CityMap.objects.create(
                name="Fortaleza Node",
                slug="fortaleza-node",
                width=3200,
                height=2200,
            )
        )

        self.interior_map = (
            CityMap.objects.create(
                name="Interior Teste",
                slug="interior-teste",
                width=900,
                height=700,
            )
        )

    def test_only_one_default_spawn_per_map(
        self
    ):

        first = (
            SpawnPoint.objects.create(
                map=self.city_map,
                name="Entrada A",
                code="entrada-a",
                x=100,
                y=100,
                is_default=True,
            )
        )

        second = (
            SpawnPoint.objects.create(
                map=self.city_map,
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

    def test_different_maps_can_have_default_spawns(
        self
    ):

        city_spawn = (
            SpawnPoint.objects.create(
                map=self.city_map,
                name="Cidade",
                code="cidade",
                x=1600,
                y=1100,
                is_default=True,
            )
        )

        interior_spawn = (
            SpawnPoint.objects.create(
                map=self.interior_map,
                name="Interior",
                code="interior",
                x=450,
                y=350,
                is_default=True,
            )
        )

        city_spawn.refresh_from_db()
        interior_spawn.refresh_from_db()

        self.assertTrue(
            city_spawn.is_default
        )

        self.assertTrue(
            interior_spawn.is_default
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
        
        def test_interaction_position_uses_offsets(
            self
        ):

            building = Building.objects.create(
                map=self.city_map,
                name="Bloco Interativo",
                slug="bloco-interativo",
                image_path=(
                    "world/img/buildings/"
                    "building_interactive.png"
                ),
                x=900,
                y=500,
                width=320,
                height=320,
                collision_width=260,
                collision_height=100,
                has_entrance=True,
                interaction_offset_x=135,
                interaction_offset_y=285,
                interaction_width=50,
                interaction_height=35,
            )

            self.assertEqual(
                building.interaction_x,
                1035,
            )

            self.assertEqual(
                building.interaction_y,
                785,
            )
            
            def test_city_sends_building_interaction(
                self
            ):

                self.complete_operator()

                Building.objects.create(
                    map=self.city_map,
                    name="Bloco Interativo",
                    slug="bloco-interativo",
                    image_path=(
                        "world/img/buildings/"
                        "building_interactive.png"
                    ),
                    x=900,
                    y=500,
                    width=320,
                    height=320,
                    collision_width=260,
                    collision_height=100,
                    has_entrance=True,
                    interaction_offset_x=135,
                    interaction_offset_y=285,
                    interaction_width=50,
                    interaction_height=35,
                )

                response = self.client.get(
                    reverse(
                        "world:city"
                    )
                )

                building = (
                    response.context[
                        "game_world"
                    ]["buildings"][0]
                )

                self.assertTrue(
                    building[
                        "interaction"
                    ]["enabled"]
                )

                self.assertEqual(
                    building[
                        "interaction"
                    ]["x"],
                    1035,
                )

                self.assertEqual(
                    building[
                        "interaction"
                    ]["type"],
                    "entrance",
                )
            
class GenericMapTests(TestCase):

    def setUp(self):

        self.faction = (
            Faction.objects.create(
                name="Cangaceiros Digitais",
                slug="cangaceiros-digitais",
                code="CD",
                symbol="CD",
                description="Factrion de teste.",
                color="#FF8A5B",
            )
        )

        self.operator = (
            Operator.objects.create_user(
                username="maptester",
                email="map@test.nexo",
                password="StrongTestPass989!",
            )
        )

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

        self.client.force_login(
            self.operator
        )

        self.interior = (
            CityMap.objects.create(
                name="Interior Teste",
                slug="interior-teste",
                width=900,
                height=700,
            )
        )

        SpawnPoint.objects.create(
            map=self.interior,
            name="Entrada Interior",
            code="interior-entry",
            x=450,
            y=350,
            is_default=True,
        )

    def test_generic_map_can_be_loaded(
        self
    ):

        response = self.client.get(
            reverse(
                "world:map",
                kwargs={
                    "map_slug":
                        "interior-teste",
                },
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        world_data = (
            response.context[
                "game_world"
            ]
        )

        self.assertEqual(
            world_data["slug"],
            "interior-teste",
        )

        self.assertEqual(
            world_data["width"],
            900,
        )

        self.assertEqual(
            world_data["height"],
            700,
        )

        self.assertEqual(
            world_data["spawn"]["x"],
            450,
        )

        self.assertEqual(
            world_data["spawn"]["y"],
            350,
        )
        
        def test_unknown_map_returns_404(
            self
        ):

            response = self.client.get(
                reverse(
                    "world:map",
                    kwargs={
                        "map_slug":
                            "mapa-do-multiverso-404",
                    },
                )
            )

            self.assertEqual(
                response.status_code,
                404,
            )
            
        def test_inactive_map_returns_404(
            self
        ):

            self.interior.is_active = False
            self.interior.save()

            response = self.client.get(
                reverse(
                    "world:map",
                    kwargs={
                        "map_slug":
                            "interior-teste",
                    },
                )
            )

            self.assertEqual(
                response.status_code,
                404,
            )