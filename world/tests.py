from django.test import TestCase
from django.urls import reverse

from operators.models import Operator


class CityAccessTests(TestCase):

    def setUp(self):

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