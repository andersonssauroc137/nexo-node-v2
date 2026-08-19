from django.test import TestCase
from django.urls import reverse
from world.models import CityMap
from operators.models import Operator

from .models import Faction


class FactionTestsBase(TestCase):

    def setUp(self):

        self.operator = (
            Operator.objects.create_user(
                username="jp01",
                email="jp01@nexo.test",
                password="StrongTestPass989!",
            )
        )

        self.terra_nova = (
            Faction.objects.create(
                name="Terra Nova",
                slug="terra-nova",
                code="TN",
                symbol="TN",
                description="Factrion de teste.",
                color="#55E39F",
                display_order=10,
            )
        )

        self.mascarados = (
            Faction.objects.create(
                name="Mascarados",
                slug="mascarados",
                code="MSK",
                symbol="M",
                description="Outra Factrion.",
                color="#A96BFF",
                display_order=20,
            )
        )

        self.client.force_login(
            self.operator
        )


class OnboardingAccessTests(
    FactionTestsBase
):

    def test_faction_is_available_first(self):

        response = self.client.get(
            reverse(
                "identity:choose_faction"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_cognitive_test_route_is_available(
        self
    ):

        response = self.client.get(
            reverse(
                "identity:cognitive_test"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )


    def test_avatar_cannot_be_skipped_to(
        self
    ):

        response = self.client.get(
            reverse(
                "identity:choose_avatar"
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "identity:choose_faction"
            ),
        )


class FactionSelectionTests(
    FactionTestsBase
):

    def test_active_factions_are_displayed(self):

        response = self.client.get(
            reverse(
                "identity:choose_faction"
            )
        )

        self.assertContains(
            response,
            "Terra Nova",
        )

        self.assertContains(
            response,
            "Mascarados",
        )

    def test_inactive_faction_is_not_displayed(self):

        self.mascarados.is_active = False
        self.mascarados.save()

        response = self.client.get(
            reverse(
                "identity:choose_faction"
            )
        )

        self.assertNotContains(
            response,
            "Mascarados",
        )

    def test_confirmation_page_does_not_save_choice(
        self
    ):

        response = self.client.get(
            reverse(
                "identity:confirm_faction",
                kwargs={
                    "faction_slug":
                        self.terra_nova.slug,
                },
            )
        )

        self.operator.refresh_from_db()

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIsNone(
            self.operator.faction
        )

    def test_confirming_faction_saves_choice(
        self
    ):

        response = self.client.post(
            reverse(
                "identity:confirm_faction",
                kwargs={
                    "faction_slug":
                        self.terra_nova.slug,
                },
            )
        )

        self.operator.refresh_from_db()

        self.assertEqual(
            self.operator.faction,
            self.terra_nova,
        )

        self.assertEqual(
            self.operator.onboarding_step,
            Operator.OnboardingStep.CHOOSE_AVATAR,
        )

        self.assertRedirects(
            response,
            reverse(
                "identity:choose_avatar"
            ),
        )

    def test_faction_cannot_be_changed_normally(
        self
    ):

        self.operator.faction = (
            self.terra_nova
        )

        self.operator.onboarding_step = (
            Operator.OnboardingStep.CHOOSE_AVATAR
        )

        self.operator.save()

        response = self.client.post(
            reverse(
                "identity:confirm_faction",
                kwargs={
                    "faction_slug":
                        self.mascarados.slug,
                },
            )
        )

        self.operator.refresh_from_db()

        self.assertEqual(
            self.operator.faction,
            self.terra_nova,
        )

        self.assertRedirects(
            response,
            reverse(
                "identity:choose_avatar"
            ),
        )

class AvatarSelectionTests(
    FactionTestsBase
):

    def setUp(self):

        super().setUp()

        self.city_map = CityMap.objects.create(
            name="Fortaleza Node",
            slug="fortaleza-node",
            width=3200,
            height=2200,
            is_active=True,
        )

        self.operator.faction = (
            self.terra_nova
        )

        self.operator.onboarding_step = (
            Operator.OnboardingStep.CHOOSE_AVATAR
        )

        self.operator.save()

    def test_avatar_page_is_available(self):

        response = self.client.get(
            reverse(
                "identity:choose_avatar"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_avatar_selection_completes_onboarding(
        self
    ):

        response = self.client.post(
            reverse(
                "identity:choose_avatar"
            ),
            {
                "presentation": "male",
                "shirt_color": "cyan",
            },
        )

        self.operator.refresh_from_db()

        self.assertEqual(
            self.operator.presentation,
            Operator.Presentation.MALE,
        )

        self.assertEqual(
            self.operator.shirt_color,
            Operator.ShirtColor.CYAN,
        )

        self.assertEqual(
            self.operator.onboarding_step,
            Operator.OnboardingStep.COMPLETED,
        )

        self.assertIsNotNone(
            self.operator.onboarding_completed_at
        )

        self.assertRedirects(
            response,
            reverse(
                "world:city"
            ),
        )

    def test_invalid_avatar_does_not_complete_onboarding(
        self
    ):

        response = self.client.post(
            reverse(
                "identity:choose_avatar"
            ),
            {
                "presentation": "robot",
                "shirt_color": "laser-pink-9000",
            },
        )

        self.operator.refresh_from_db()

        self.assertEqual(
            self.operator.onboarding_step,
            Operator.OnboardingStep.CHOOSE_AVATAR,
        )

        self.assertEqual(
            response.status_code,
            200,
        )