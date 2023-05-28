from product_db import ProductDB


class TestProductDB:
    def test_from_yaml(self):
        db_path = 'tests/db/products.yaml'
        product_db = ProductDB.from_yaml(db_path)
        expected_products = {
            1: {'barcode': 1, 'name': 'Beans', 'unit_price': 1.5},
            2: {'barcode': 2, 'name': 'Onions', 'unit_price': 0.29, 'units': 'kg'},
        }
        assert product_db._products == expected_products
