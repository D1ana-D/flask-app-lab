import unittest
from app import app
from app.products.views import products_table

class ProductsCRUDTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SECRET_KEY"] = "test-secret-key"
        self.client = app.test_client()

    def test_1_add_product(self):
        response = self.client.post("/products/product/add", data={
            "name": "Тестовий Ноутбук",
            "content": "Опис тестового ноутбука для юніт-тесту",
            "price": "999.99",
            "category": "Computers",
            "quantity": "5"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_2_products_list(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)

    def test_3_product_detail(self):
        all_items = products_table.all()
        if all_items:
            prod_id = all_items[0]['id']
            response = self.client.get(f"/products/product/{prod_id}")
            self.assertEqual(response.status_code, 200)

    def test_4_delete_product(self):
        all_items = products_table.all()
        if all_items:
            prod_id = all_items[0]['id']
            response = self.client.post(f"/products/product/{prod_id}/delete", follow_redirects=True)
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()