import warnings
from typing import Optional

from shoppingbasket.invoice import Invoice
from shoppingbasket.basket_item import BasketItem
from shoppingbasket.product_db import ProductDB
from shoppingbasket.promotions import Promotion


class Basket:
    """Keeps track of items in a shopping basket.

    Items can either be added to the basket manually (by creating a new item),
    or by scanning a barcode that is looked up in the product database.
    """

    def __init__(self,
                 products: Optional[ProductDB] = None,
                 basket_items: list[BasketItem] = None) -> None:
        """Initialise a basket.

        Args:
            products: A database of products, keyed by barcode.
            basket_items: A list of items in the basket.
        """

        self.products = products
        self.basket_items = [] if basket_items is None else basket_items

    def add_item(self,
                 name: str,
                 unit_price: float,
                 *args,
                 barcode: Optional[int] = None,
                 units: Optional[str] = None,
                 quantity: float = 1.0,
                 **kwargs) -> None:
        """Add an item to the basket.

        Args:
            name: The name of the item.
            unit_price: The price of the item.
            *args: Additional arguments to pass to BasketItem.
            barcode: The barcode of the item. Defaults to None.
            units: The units of the item. Defaults to None.
            quantity: The amount of the item. Defaults to 1.0.
            **kwargs: Additional keyword arguments to pass to BasketItem.
        """

        basket_item = BasketItem(name,
                                 unit_price,
                                 *args,
                                 barcode=barcode,
                                 units=units,
                                 quantity=quantity,
                                 **kwargs)
        self.basket_items.append(basket_item)

    def add_item_from_barcode(self,
                              barcode: int,
                              quantity: float = 1.0) -> None:
        """Add an item to the basket using barcode.

        Args:
            barcode: The barcode of the item to add.
            quantity: The amount of the item to add. Defaults to 1.0.

        Raises:
            ValueError: If product_db is None.
        """

        if self.products is None:
            raise (ValueError("Cannot add from barcode without products."))

        try:
            product = self.products[barcode]
            self.add_item(**product, quantity=quantity)
        except KeyError:
            # Could raise an error, but this allows continuing
            warnings.warn(f"Barcode {barcode} not found in product database. "
                          "Item not added to basket.")

    def generate_invoice(
            self,
            promotions: Optional[list[Promotion]] = None
    ) -> 'Invoice':
        """Get an invoice for items in the basket."""
        return Invoice(self.basket_items, promotions=promotions)
