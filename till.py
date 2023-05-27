from dataclasses import dataclass

from product_db import Product


@dataclass
class TillItem:
    product: Product
    amount: float = 1.0

    def to_receipt_string(self) -> str:
        price_gbp = f"£{self.price:.2f}"
        receipt_string = f"{self.product.name}\t\t{price_gbp}"

        # If not simply price per item, add extra line with details
        # e.g. 1.34kg @ £0.612/kg
        if self.product.units != 'per_item':
            amount = f"{self.amount}{self.product.units}"
            rate = f"£{self.product.unit_price}/{self.product.units}"
            receipt_string += f"\n\t{amount} @ {rate}"

        return receipt_string

    @property
    def price(self) -> float:
        return round(self.product.unit_price * self.amount, 2)
