from dataclasses import dataclass
from typing import Iterable, Optional

from tabulate import tabulate, SEPARATING_LINE

from basket_item import BasketItem
from product_db import ProductDB
from promotions import Promotions


@dataclass
class Basket:
    """Keeps track of items in a shopping basket."""

    def __init__(self,
                 product_db: Optional[ProductDB] = None,
                 basket_items: Optional['BasketItem'] = None,
                 promotions: Optional[Promotions] = None) -> None:
        self.product_db = product_db
        self.basket_items = basket_items or []
        self.promotions = promotions

    def add_item(self, basket_item: 'BasketItem') -> None:
        """Add an item to the basket."""
        self.basket_items.append(basket_item)

    def add_item_from_barcode(self, barcode: int, amount: float = 1.0) -> None:
        """Add an item to the basket.

        Args:
            barcode: The barcode of the item to add.
            amount: The amount of the item to add. Defaults to 1.0.

        Raises:
            ValueError: If product_db is None.
        """

        if self.product_db is None:
            raise (ValueError("Cannot add from barcode without product_db."))

        product = self.product_db[barcode]
        basket_item = BasketItem(**product, amount=amount)
        self.add_item(basket_item)

    def generate_invoice(self) -> 'Invoice':
        """Get an invoice for items in the basket."""
        return Invoice(self.basket_items, self.promotions)


class Invoice:
    """A receipt for a shopping basket."""

    def __init__(self,
                 basket_items: Iterable[BasketItem],
                 promotions: Optional[Promotions] = None) -> None:
        self.basket_items = basket_items
        self.discounts = self.calculate_discounts(promotions)

    def calculate_discounts(self, promotions: Promotions | None) -> list[BasketItem]:
        """Calculate the discounts for the basket."""
        if promotions is None:
            return []
        return promotions.list_discounts(self.basket_items)

    @property
    def subtotal(self) -> float:
        """The total price of items in the basket before discounts."""
        return sum(item.line_price for item in self.basket_items)

    @property
    def discount_total(self) -> float:
        """The total price of discounts in the basket."""
        return sum(discount.line_price for discount in self.discounts)

    @property
    def total(self) -> float:
        """The total price of items in the basket after discounts."""
        return self.subtotal + self.discount_total

    def to_string(self) -> str:
        """Generate an invoice for the basket."""
        receipt = self._get_product_lines()

        if self.discount_total != 0:
            receipt += self._get_product_lines()

        receipt.append(SEPARATING_LINE)
        receipt.append([f"Total to pay", f"£{self.total:.2f}"])

        return tabulate(receipt)

    def _get_product_lines(self) -> list[list[str]]:
        """The lines for the products in the basket."""
        product_lines = [['Item', 'Price'], SEPARATING_LINE]
        product_lines += [[f"{item.description}", f"£{item.line_price:.2f}"]
                          for item in self.basket_items]
        product_lines += SEPARATING_LINE
        product_lines += [[f"Sub-total", f"£{self.subtotal:.2f}"]]
        return product_lines

    def _get_discount_lines(self) -> list[list[str]]:
        """The lines for the discounts in the basket."""
        discount_lines = [SEPARATING_LINE, ['Savings']]

        for discount in self.discounts:
            discount_lines.append([f"{discount.name}",
                                   f"£{discount.line_price:.2f}"])

        discount_lines.append(SEPARATING_LINE)
        discount_lines.append([f"Total savings",
                               f"£{self.discount_total:.2f}"])
        return discount_lines
