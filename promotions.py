from dataclasses import dataclass
from typing import Protocol, Iterable

import more_itertools


@dataclass
class Promotions:
    promotions: list['PromotionModel']

    def calculate_discounts(self, items: list['BasketItem']):
        """Calculate the discount for a list of items.
        
        Args:
            items: A list of items.
            
        """

        for promotion in self.promotions:
            for discount in promotion.calculate(items):
                yield promotion.name, discount


@dataclass
class PromotionModel(Protocol):
    """A discount that can be applied to a shopping basket items."""

    def calculate_discounts(self,
                            items: list['BasketItem']) -> tuple[str, float]:
        """Calculate the discount for a list of items.

        Args:
            items: A list of items.

        Returns:
            The discount.
        """
        ...


@dataclass
class MForN(PromotionModel):
    name: str
    barcode: int
    m: int
    n: int

    def calculate(self, items: list['BasketItem']) -> list[float]:
        eligible_items = [item for item in items
                          if item.barcode == self.barcode]
        if len(eligible_items) < self.m:
            return []

        unit_price = eligible_items[0].unit_price

        # Could just do len(eligible_items) since this only applied to 'per
        # item' products, but this works if in future we have item.amount > 1
        # for any reason.
        amount = sum(item.amount for item in eligible_items)
        return [unit_price * (self.m - self.n)] * int(amount // self.m)


@dataclass
class MForNPounds(PromotionModel):
    name: str
    barcodes: set[int]
    m: int
    n: float

    def calculate(self, items: list['BasketItem']) -> Iterable[float]:
        """Calculate the discount for a list of items.

        Args:
            items: A list of items.

        Returns:
            The discount.
        """

        items_in_promotion = self.get_eligible_items(items)

        # Apply to most expensive products first, for happy customers.
        items_in_promotion.sort(reverse=True, key=lambda item: item.price)

        for items in more_itertools.chunked(items_in_promotion, self.m):
            if len(items) < self.m:
                break

            items_subtotal = sum(item.price for item in items)
            discount_amount = items_subtotal - self.n
            if discount_amount > 0:
                yield round(discount_amount, 2)

    def get_eligible_items(self, items: list['BasketItem']) -> list['BasketItem']:
        """Get the items that are eligible for the discount.

        Args:
            items: A list of items.

        Returns:
            A list of eligible items.
        """
        return [item for item in items if
                item.barcode in self.barcodes]
