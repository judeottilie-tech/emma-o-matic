from django.test import Client, SimpleTestCase

from machine import views


class MachineTests(SimpleTestCase):
    def setUp(self):
        views.coins = 0
        views.inventory = [5, 5, 5]

    def insert_coins(self, count):
        for _ in range(count):
            self.client.put(
                "/", data={"coin": 1}, content_type="application/json"
            )

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

    def test_return_coins(self):
        self.insert_coins(3)
        response = self.client.delete("/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response["X-Coins"], "3")
        self.assertEqual(views.coins, 0)

    def test_wrong_method_on_inventory(self):
        client = Client(enforce_csrf_checks=True)
        response = client.put("/inventory")
        self.assertEqual(response.status_code, 405)

    def test_purchase_success(self):
        self.insert_coins(2)
        response = self.client.put("/inventory/0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"quantity": 1})
        self.assertEqual(response["X-Coins"], "0")
        self.assertEqual(response["X-Inventory-Remaining"], "4")
        self.assertEqual(views.coins, 0)

    def test_purchase_returns_change(self):
        self.insert_coins(3)
        response = self.client.put("/inventory/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"quantity": 1})
        self.assertEqual(response["X-Coins"], "1")
        self.assertEqual(response["X-Inventory-Remaining"], "4")
        self.assertEqual(views.coins, 0)

    def test_purchase_not_enough_coins(self):
        self.insert_coins(1)
        response = self.client.put("/inventory/0")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response["X-Coins"], "1")
        self.assertEqual(views.coins, 1)
        self.assertEqual(views.inventory, [5, 5, 5])

    def test_purchase_out_of_stock(self):
        views.inventory = [5, 0, 5]
        self.insert_coins(2)
        response = self.client.put("/inventory/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["X-Coins"], "2")
        self.assertEqual(views.coins, 2)

    def test_out_of_stock_beats_not_enough_coins(self):
        views.inventory = [5, 0, 5]
        self.insert_coins(1)
        response = self.client.put("/inventory/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["X-Coins"], "1")
        self.assertEqual(views.coins, 1)

    def test_get_one_item(self):
        response = self.client.get("/inventory/0") 
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json(), 5)  

    def test_invalid_id(self):
        self.insert_coins(1)
        response = self.client.put("/inventory/7")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["X-Coins"], "1")

    def test_wrong_method_on_coins(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post("/")
        self.assertEqual(response.status_code, 405)
