from django.test import TestCase
from django.urls import reverse

from .models import Operator


class OperatorModelTests(TestCase):

    def test_operator_generates_network_id(self):

        operator = Operator.objects.create_user(
            username="a9",
            email="a9@nexo.test",
            password="test-password-123",
        )

        self.assertTrue(
            operator.network_id.startswith(
                "FN-"
            )
        )

        self.assertEqual(
            len(operator.network_id),
            9,
        )

    def test_default_onboarding_step(self):

        operator = Operator.objects.create_user(
            username="v11",
            email="v11@nexo.test",
            password="test-password-123",
        )

        self.assertEqual(
            operator.onboarding_step,
            Operator.OnboardingStep.CHOOSE_FACTION,
        )

    def test_operator_starts_without_faction(self):

        operator = Operator.objects.create_user(
            username="a9-faction-test",
            email="a9-faction@nexo.test",
            password="StrongTestPass989!",
        )

        self.assertIsNone(
            operator.faction
        )


class OperatorRegistrationTests(TestCase):

    def test_registration_creates_operator(self):

        response = self.client.post(
            reverse(
                "operators:register"
            ),
            {
                "username": "ghostbyte",
                "email": "ghost@nexo.test",
                "password1": "StrongTestPass989!",
                "password2": "StrongTestPass989!",
            },
        )

        operator = Operator.objects.get(
            username="ghostbyte"
        )

        self.assertIsNotNone(
            operator.network_id
        )

        self.assertEqual(
            operator.onboarding_step,
            Operator.OnboardingStep.CHOOSE_FACTION,
        )

        self.assertRedirects(
            response,
            reverse(
                "identity:choose_faction"
            ),
        )

    def test_duplicate_email_is_rejected(self):

        Operator.objects.create_user(
            username="operator1",
            email="same@nexo.test",
            password="StrongTestPass989!",
        )

        response = self.client.post(
            reverse(
                "operators:register"
            ),
            {
                "username": "operator2",
                "email": "same@nexo.test",
                "password1": "StrongTestPass989!",
                "password2": "StrongTestPass989!",
            },
        )

        self.assertEqual(
            Operator.objects.filter(
                email="same@nexo.test"
            ).count(),
            1,
        )

        self.assertEqual(
            response.status_code,
            200,
        )