from typing import NamedTuple

import yaml


class ProductDB:
    """A database of products, indexed by barcode."""

    def __init__(self, products: list['Product']) -> None:
        self._products = {product.barcode: product for product in products}

    def __getitem__(self, barcode: int) -> 'Product':
        """Get a product by barcode."""
        return self._products[barcode]

    @staticmethod
    def from_yaml(db_path: str) -> 'ProductDB':
        """Load a product database from a YAML file.

        The YAML file must be structured as a list of dictionaries, where each
        dictionary represents a product. The dictionary must contain the keys
        'barcode', 'name', and 'unit_price'. The key 'units' is optional, and
        defaults to 'per_item'.

        Args:
            db_path: The path to the YAML file.

        Returns:
            A ProductDB object.
        """

        with open(db_path, 'r') as f:
            product_dicts = yaml.safe_load(f)
        return ProductDB.from_dicts(product_dicts)

    @staticmethod
    def from_dicts(product_dicts: list[dict[str, str | float]]) -> 'ProductDB':
        """Load a product database from a list of dictionaries.

        Args:
            product_dicts: A list of dictionaries, where each dictionary
                represents a product. The dictionary must contain the keys
                'barcode', 'name', and 'unit_price'. The key 'units' is
                optional, and defaults to 'per_item'.

        Returns:
            A ProductDB object.
        """

        products = [Product.from_dict(product_dict)
                    for product_dict in product_dicts]
        return ProductDB(products)


class Product(NamedTuple):
    """A product in the product database.

    Attributes:
        barcode: The product's barcode.
        name: The product's name.
        unit_price: The product's unit price.
        units: The product's units, e.g. 'per_item' or 'per_kg'.
    """

    barcode: int
    name: str
    unit_price: float
    units: str

    @staticmethod
    def from_dict(product_dict: dict[str, str | float],
                  default_units: str = 'per_item') -> 'Product':
        """Create a Product from a dictionary.

        Args:
            product_dict: A dictionary representing a product. The dictionary
                must contain the keys 'barcode', 'name', and 'unit_price'. The
                key 'units' is optional, and defaults to 'per_item'.
            default_units: The units to use if 'units' is not specified in
                product_dict.

        Returns:
            A Product object.
        """
        
        barcode = product_dict['barcode']
        name = product_dict['name']
        unit_price = product_dict['unit_price']
        units = product_dict.get('units', default_units)
        return Product(barcode, name, unit_price, units)
