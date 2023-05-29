import yaml


class ProductDB:
    """A database of products, indexed by barcode."""

    def __init__(self, products: list[dict]) -> None:
        self._products = {product['barcode']: product for product in products}

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
            return ProductDB(yaml.safe_load(f))
