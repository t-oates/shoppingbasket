import warnings
from dataclasses import dataclass
from typing import Iterable, Optional, Iterator

from texttable import Texttable

from shoppingbasket.basket_item import BasketItem, Discount
from shoppingbasket.product_db import ProductDB
from shoppingbasket.promotions import Promotion


class Basket:
    """Keeps track of items in a shopping basket.

    Items can either be added to the basket manually (by creating a new item),
    or by scanning a barcode that is looked up in the product database.
    """

    def __init__(self,
                 products: Optional[ProductDB] = None,
                 basket_items: list[BasketItem] = None,
                 promotions: Optional[list[Promotion]] = None) -> None:
        """Initialise a basket.

        Args:
            products: A database of products, keyed by barcode.
            basket_items: A list of items in the basket.
            promotions: A list of promotions that can be applied to the basket.
        """

        self.products = products
        self.basket_items = [] if basket_items is None else basket_items
        self.promotions = [] if promotions is None else promotions

    def add_item(self, basket_item: 'BasketItem') -> None:
        """Add an item to the basket.

        Args:
            basket_item: The item to add.
        """

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
            self.add_item(BasketItem(**product, quantity=quantity))
        except KeyError:
            # Could raise an error, but this allows continuing
            warnings.warn(f"Barcode {barcode} not found in product database. "
                          "Item not added to basket.")

    def generate_invoice(self) -> 'Invoice':
        """Get an invoice for items in the basket."""
        return Invoice(self.basket_items, self.promotions)


@dataclass
class Invoice:
    """An invoice for a shopping basket."""

    basket_items: Iterable[BasketItem]
    promotions: Optional[list[Promotion]] = None

    def __post_init__(self):
        self.discounts = list(self.get_discounts(self.promotions))

    def get_discounts(self, promotions: Optional[list[Promotion]]) -> Iterator[
        Discount]:
        """Calculate the discounts for the basket."""
        if promotions is not None:
            for promotion in promotions:
                yield from promotion.get_discounts(self.basket_items)

    @property
    def subtotal(self) -> float:
        """The total price of items in the basket before discounts."""
        return sum(item.line_price for item in self.basket_items)

    @property
    def discount_total(self) -> float:
        """The total price of discounts in the basket."""
        total = sum(discount.line_price for discount in self.discounts)
        return round(total, 2)

    @property
    def total(self) -> float:
        """The total price of items in the basket after discounts."""
        return self.subtotal + self.discount_total

    def to_string(self) -> str:
        """Generate a printable invoice in table format."""

        # Line to separate sections of the invoice
        row_separator = ['-' * 20, '-' * 6]

        # Create a table for the invoice
        tbl = Texttable()
        tbl.set_deco(Texttable.HEADER)
        tbl.set_header_align(['l', 'r'])
        tbl.set_cols_align(['l', 'r'])
        tbl.set_cols_valign(['m', 'b'])
        tbl.header(['Item', 'Price'])

        # Add basket items
        tbl.add_rows(self._get_product_lines(), header=False)
        tbl.add_row(row_separator)
        tbl.add_row([f"Sub-total", f"£{self.subtotal:.2f}"])

        # Add discounts
        if self.discount_total != 0:
            tbl.add_row(row_separator)
            tbl.add_row(['Savings', ''])
            tbl.add_row(row_separator)
            tbl.add_rows(self._get_discount_lines(), header=False)
            tbl.add_row(row_separator)
            tbl.add_row([f"Total savings", f"£{self.discount_total:.2f}"])

        tbl.add_row(row_separator)
        tbl.add_row([f"Total to pay", f"£{self.total:.2f}"])

        return tbl.draw()

    def _get_product_lines(self) -> list[list[str]]:
        """The lines for the products in the basket."""
        product_lines = [[f"{item.description}", f"£{item.line_price:.2f}"]
                         for item in self.basket_items]
        return product_lines

    def _get_discount_lines(self) -> list[list[str]]:
        """The lines for the discounts in the basket."""

        return [[f"{discount.name}", f"£{discount.line_price:.2f}"]
                for discount in self.discounts]
