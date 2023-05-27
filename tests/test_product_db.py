import pytest

from product_db import ProductDB, Product


@pytest.fixture
def products_as_dict():
    return {
        1: Product(1, 'Beans', 1.5, 'per_item'),
        2: Product(2, 'Onions', 0.29, 'kg'),
    }


class TestProductDB:
    def test_from_yaml(self, products_as_dict):
        db_path = 'tests/db/products.yaml'
        product_db = ProductDB.from_yaml(db_path)
        assert product_db._products == products_as_dict

    def test_from_dicts(self, products_as_dict):
        product_dicts = [
            {'barcode': 1, 'name': 'Beans', 'unit_price': 1.5},
            {'barcode': 2, 'name': 'Onions', 'unit_price': 0.29, 'units': 'kg'},
        ]
        product_db = ProductDB.from_dicts(product_dicts)
        assert product_db._products == products_as_dict


class TestProduct:
    def test_from_dict(self):
        #  Confirms that the default value for units is 'per_item'
        product_dict = {'barcode': 1, 'name': 'Beans', 'unit_price': 1.5}
        product = Product.from_dict(product_dict)
        assert product == Product(1, 'Beans', 1.5, 'per_item')

    def test_from_dict_with_units(self):
        product_dict = {'barcode': 2, 'name': 'Onions',
                        'unit_price': 0.29, 'units': 'kg'}
        product = Product.from_dict(product_dict)
        assert product == Product(2, 'Onions', 0.29, 'kg')
