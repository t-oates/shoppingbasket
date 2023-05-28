from dataclasses import dataclass
from typing import NamedTuple, Iterable

from product_db import Product, ProductDB
from promotions import PromotionModel, Promotions


class BasketManager:
    """Keeps track of items in a shopping basket.

    Attributes:
        product_db: The product database.
        basket_items: A list of BasketItems.
    """

    def __init__(self,
                 product_db: ProductDB,
                 promotions: Promotions | None = None) -> None:
        self.product_db = product_db
        self.promotions = promotions or Promotions([])
        self.basket_items = []

    def add_item(self, barcode: int, amount: float = 1.0) -> None:
        """Add an item to the basket.

        Args:
            barcode: The barcode of the item to add.
            amount: The amount of the item to add. Defaults to 1.0.
        """

        product = self.product_db[barcode]
        basket_item = BasketItem(product, amount)
        self.basket_items.append(basket_item)

    def print_receipt(self) -> None:
        """Print a receipt for the items in the basket."""

        receipt = ""
        for item in self.basket_items:
            receipt_line = item.to_receipt_line()
            receipt += (f"\n{receipt_line.description}\t\t\t\t"
                        f"£{receipt_line.price:.2f}")

        receipt += "\n-------------------------"
        receipt += f"\nSubtotal\t\t\t£{self.subtotal:.2f}"

        if self.discount_total > 0:
            receipt += "\n-------------------------"
            receipt += "\nSavings:"
            for name, discount_amount in self.discounts:
                receipt += f"\n{name}\t\t\t£-{discount_amount:.2f}"
            receipt += f"\nTotal savings\t\t\t£-{self.discount_total:.2f}"

        receipt += "\n-------------------------"
        receipt += f"\nTotal\t\t\t\t£{self.total:.2f}"

        print(receipt)

    @property
    def subtotal(self) -> float:
        """The total price of items in the basket before discounts."""
        return sum(item.price for item in self.basket_items)

    @property
    def discounts(self) -> Iterable[tuple[str, float]]:
        return self.promotions.calculate_discounts(self.basket_items)

    @property
    def discount_total(self) -> float:
        return sum(discount_amount for _, discount_amount in self.discounts)

    @property
    def total(self) -> float:
        return self.subtotal - self.discount_total


@dataclass
class BasketItem:
    """An item in a shopping basket.

    Attributes:
        product: The product.
        amount: The amount of the product.
    """

    product: Product
    amount: float = 1.0

    def to_receipt_line(self) -> 'ReceiptLine':
        """Get a string representation of the item for a receipt."""

        desc = self.product.name

        # If not simply price per item, add extra line with details
        # e.g. 1.34kg @ £0.612/kg
        if self.product.units != 'per_item':
            amount = f"{self.amount}{self.product.units}"
            rate = f"£{self.product.unit_price}/{self.product.units}"
            desc += f"\n{amount} @ {rate}"

        return ReceiptLine(desc, self.price)

    @property
    def price(self) -> float:
        """The price of the item."""
        return round(self.product.unit_price * self.amount, 2)


class ReceiptLine(NamedTuple):
    """Details needed to list item on a receipt."""
    description: str
    price: float
