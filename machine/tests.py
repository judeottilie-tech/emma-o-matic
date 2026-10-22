from django.test import SimpleTestCase

from machine import views


class MachineTests(SimpleTestCase):
    def setUp(self):
        views.coins = 0
        views.inventory = [5, 5, 5]

    def test_get_inventory(self):
        response = self.client.get("/inventory")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [5, 5, 5])

    def test_insert_coin(self):
        response = self.client.put(
            "/", data={"coin": 1}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response["X-Coins"], "1")

    def insert_coins(self, count):
        for _ in range(count):
            self.client.put(
                "/", data={"coin": 1}, content_type="application/json"
            )

    def test_return_coins(self):
        self.insert_coins(3)
        response = self.client.delete("/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response["X-Coins"], "3")
        self.assertEqual(views.coins, 0)
