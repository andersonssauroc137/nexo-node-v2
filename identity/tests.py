from django.test import TestCase
from django.urls import reverse

from operators.models import Operator


class OnboardingAccessTests(TestCase):

    def setUp(self):

        self.operator = (
            Operator.objects.create_user(
                username="jp01",
                email="jp01@nexo.test",
                password="StrongTestPass989!",
            )
        )

        self.client.force_login(
            self.operator
        )

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