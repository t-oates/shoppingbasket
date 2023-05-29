from dataclasses import dataclass
from typing import Iterable, Optional, Iterator

from texttable import Texttable

from shoppingbasket.basket_item import BasketItem, Discount
from shoppingbasket.promotions import Promotion


@dataclass
class Invoice:
    """An invoice for a shopping basket."""

    basket_items: Iterable[BasketItem]
    promotions: Optional[list[Promotion]] = None

    def __post_init__(self):
        self.discounts = list(self.get_discounts())

    def get_discounts(self) -> Iterator[Discount]:
        """Calculate the discounts for the basket."""
        if self.promotions is not None:
            for promotion in self.promotions:
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
