from django.test import TestCase
from django.urls import reverse


class CoreViewsTests(TestCase):

    def test_home_returns_200(self):
        response = self.client.get(
            reverse("core:home")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_health_returns_ok(self):
        response = self.client.get(
            reverse("core:health")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.json()["status"],
            "ok",
        )