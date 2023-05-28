from dataclasses import dataclass

from product_db import Product


class TillManager:
    def __init__(self, product_db) -> None:
        self.product_db = product_db
        self.till_items = []

    def add_item(self, barcode: int, amount: float = 1.0) -> None:
        product = self.product_db[barcode]
        till_item = TillItem(product, amount)
        self.till_items.append(till_item)

    def print_receipt(self) -> None:
        receipt = ""
        for item in self.till_items:
            receipt += item.to_receipt_string() + "\n"
        receipt += "----\t\t\t\t-----\n"
        receipt += f"Subtotal\t\t\t\t£{self.subtotal:.2f}"
        print(receipt)

    @property
    def subtotal(self) -> float:
        return sum(item.price for item in self.till_items)


@dataclass
class TillItem:
    product: Product
    amount: float = 1.0

    def to_receipt_string(self) -> str:
        price_gbp = f"£{self.price:.2f}"
        receipt_string = f"{self.product.name:<20}{price_gbp}"

        # If not simply price per item, add extra line with details
        # e.g. 1.34kg @ £0.612/kg
        if self.product.units != 'per_item':
            amount = f"{self.amount}{self.product.units}"
            rate = f"£{self.product.unit_price}/{self.product.units}"
            receipt_string += f"\n{amount} @ {rate}"

        return receipt_string

    @property
    def price(self) -> float:
        return round(self.product.unit_price * self.amount, 2)
