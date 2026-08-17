from django.test import TestCase
from django.urls import reverse

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

    def test_cognitive_test_cannot_be_skipped_to(
        self
    ):

        response = self.client.get(
            reverse(
                "identity:cognitive_test"
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "identity:choose_faction"
            ),
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
            Operator.OnboardingStep.COGNITIVE_TEST,
        )

        self.assertRedirects(
            response,
            reverse(
                "identity:cognitive_test"
            ),
        )

    def test_faction_cannot_be_changed_normally(
        self
    ):

        self.operator.faction = (
            self.terra_nova
        )

        self.operator.onboarding_step = (
            Operator.OnboardingStep.COGNITIVE_TEST
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
                "identity:cognitive_test"
            ),
        )