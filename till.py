from dataclasses import dataclass


@dataclass
class TillItem:
    barcode: int
    name: str
    unit_price: float
    units: str = 'per_item'
    amount: float = 1.0

    def to_receipt_string(self) -> str:
        price_gbp = f"£{self.price:.2f}"
        receipt_string = f"{self.name}\t\t{price_gbp}"

        # If not simply price per item, add extra line with details
        # e.g. 1.34kg @ £0.612/kg
        if self.units != 'per_item':
            amount = f"{self.amount}{self.units}"
            rate = f"£{self.unit_price}/{self.units}"
            receipt_string += f"\n\t{amount} @ {rate}"

        return receipt_string

    @property
    def price(self) -> float:
        return round(self.unit_price * self.amount, 2)
