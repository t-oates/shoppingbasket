from dataclasses import dataclass
from typing import Protocol

import more_itertools

from basket_item import BasketItem


@dataclass
class Promotions:
    promotions: list['Promotion']

    def list_discounts(self, items: list['BasketItem']):
        """Calculate the discount for a list of items.
        
        Args:
            items: A list of items.
            
        """

        return [discount for promotion in self.promotions
                for discount in promotion.list_discounts(items)]


@dataclass
class Promotion(Protocol):
    """A discount that can be applied to a shopping basket items."""

    def list_discounts(self, basket_items: list[BasketItem]) -> list[BasketItem]:
        """Calculate the discount for a list of items.

        Args:
            basket_items: A list of items.

        Returns:
            The discount.
        """
        ...


@dataclass
class MForN(Promotion):
    name: str
    barcode: int
    m: int
    n: int

    def list_discounts(self, items: list['BasketItem']) -> list[BasketItem]:
        eligible_items = [item for item in items
                          if item.barcode == self.barcode]
        if len(eligible_items) < self.m:
            return []

        unit_price = eligible_items[0].unit_price
        discount_amount = unit_price * (self.m - self.n)
        discount = BasketItem(self.name, discount_amount, amount=-1)

        num_discounts = len(eligible_items) // self.m
        return [discount] * num_discounts


@dataclass
class MForNPounds(Promotion):
    name: str
    barcodes: set[int]
    m: int
    n: float

    def list_discounts(self, items: list['BasketItem']) -> list[BasketItem]:
        """Calculate the discount for a list of items.

        Args:
            items: A list of items.

        Returns:
            The discount.
        """

        items_in_promotion = self.get_eligible_items(items)

        # Apply to most expensive products first, for happy customers.
        items_in_promotion.sort(reverse=True, key=lambda item: item.price)


        discounts = []
        for items in more_itertools.chunked(items_in_promotion, self.m):
            if len(items) < self.m:
                break

            items_subtotal = sum(item.price for item in items)
            discount_amount = items_subtotal - self.n
            if discount_amount > 0:
                discounts.append(BasketItem(self.name, discount_amount, amount=-1))

        return discounts

    def get_eligible_items(self, items: list['BasketItem']) -> list['BasketItem']:
        """Get the items that are eligible for the discount.

        Args:
            items: A list of items.

        Returns:
            A list of eligible items.
        """
        return [item for item in items if
                item.barcode in self.barcodes]
