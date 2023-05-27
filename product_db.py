from typing import NamedTuple

import yaml


class ProductDB:
    def __init__(self, products: list['Product']) -> None:
        self._products = {product.barcode: product for product in products}

    def __getitem__(self, barcode: int) -> 'Product':
        return self._products[barcode]

    @staticmethod
    def from_yaml(db_path: str) -> 'ProductDB':
        with open(db_path, 'r') as f:
            product_dicts = yaml.safe_load(f)
        return ProductDB.from_dicts(product_dicts)

    @staticmethod
    def from_dicts(product_dicts: list[dict[str, str | float]]) -> 'ProductDB':
        products = [Product.from_dict(product_dict)
                    for product_dict in product_dicts]
        return ProductDB(products)


class Product(NamedTuple):
    barcode: int
    name: str
    unit_price: float
    units: str

    @staticmethod
    def from_dict(product_dict: dict[str, str | float],
                  default_units: str = 'per_item') -> 'Product':
        barcode = product_dict['barcode']
        name = product_dict['name']
        unit_price = product_dict['unit_price']
        units = product_dict.get('units', default_units)
        return Product(barcode, name, unit_price, units)
