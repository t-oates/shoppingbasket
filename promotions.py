from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from typing import Iterator, Iterable

import more_itertools

from basket_item import BasketItem, Discount


@dataclass
class Promotion(ABC):
    """A discount that can be applied to a shopping basket items."""

    name: str
    eligible_barcodes: set[int]

    def list_eligible_items(self, basket_items: list[BasketItem]) -> list[BasketItem]:
        """Get the basket_items that are eligible for the promotion."""
        return [item for item in basket_items
                if item.barcode in self.eligible_barcodes]

    @abstractmethod
    def get_discounts(self, basket_items: list[BasketItem]) -> Iterable[Discount]:
        """Calculate the discounts for a list of items.

        Args:
            basket_items: A list of items.

        Returns:
            The discounts.
        """


@dataclass
class MForN(Promotion):
    """Promo where you get m items for the price of n.

    For example, 3 for the price of 2. This can only be applied to are group of
    items that are the same product, e.g. 3 cans of beans (this doesn't work
    for, e.g. "buy 3 get the cheapest free" for different products).

    If multiple barcodes are supplied, the promotion will be applied to each
    barcode separately.
    """

    name: str
    eligible_barcodes: set[int]
    m: int = 3  # Number of items required for discount
    n: int = 2  # Number of items that are paid for

    def get_discounts(self, basket_items: list[BasketItem]) -> Iterator[Discount]:
        eligible_items = self.list_eligible_items(basket_items)
        item_counts = Counter(eligible_items)
        for item, item_count in item_counts.items():
            yield from self._get_discounts_single_barcode(item, item_count)

    def _get_discounts_single_barcode(
            self,
            basket_item: BasketItem,
            item_count: int
    ) -> Iterator[Discount]:
        """Calculate the discounts for a single barcode.

        The discount amount for each individual discount will simply be the
        unit price of the item multiplied by the number of free items in the
        discount (m - n). We then apply the discount repeatedly for how many
        groups size m there are.

        Args:
            basket_item: A basket item.
            item_count: The number of items with the same barcode.

        Returns:
            The discounts.
        """

        discount_amount = basket_item.unit_price * (self.m - self.n)
        discount = Discount(self.name, discount_amount)
        num_discounts = item_count // self.m
        for _ in range(num_discounts):
            yield discount


@dataclass
class MForNPounds(Promotion):
    """Promo where items bought in a set are discounted to a fixed price.

    These items can be different products that are grouped under a single
    promotion (e.g. 3 ales from a set for £6)

    If the number of eligible items is not a multiple of m, the discount will
    be applied to the most expensive items, to keep customers happy.
    """

    name: str
    eligible_barcodes: set[int]
    m: int = 3  # Number of items required for discount
    n: float = 6.0  # Price to pay for m items

    def get_discounts(self, basket_items: list[BasketItem]) -> Iterator[Discount]:
        eligible_items = self.list_eligible_items(basket_items)

        # Sort so we discount most expensive items first
        eligible_items.sort(reverse=True, key=lambda item: item.line_price)

        # Split into groups of m items
        item_groups = more_itertools.chunked(eligible_items, self.m)

        for items in item_groups:
            if len(items) < self.m:
                break
            discount = self._get_discount(items)
            if discount.line_price < 0:
                yield discount

    def _get_discount(self, items: list[BasketItem]) -> Discount:
        """Calculate the discount for a set of items.

        Args:
            items: A list of items.

        Returns:
            The discount.
        """

        items_subtotal = sum(item.line_price for item in items)
        discount_amount = items_subtotal - self.n
        return Discount(self.name, discount_amount)
