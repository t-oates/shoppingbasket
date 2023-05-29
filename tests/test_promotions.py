import pytest

from basket_item import BasketItem
from product_db import ProductDB
from promotions import MForNPounds


@pytest.fixture
def product_db():
    db_path = 'tests/db/full_product_db.yaml'
    return ProductDB.from_yaml(db_path)


class TestMForNPoundsSingle:
    barcodes = {4}  # Coke
    promotion = MForNPounds("Coke 2 for £1", barcodes, 2, 1.0)

    def test_not_exact_multiple(self, product_db):
        """Test that the discount is calculated correctly when the number of
        eligible items is not an exact multiple of m."""
        basket_barcodes = [1, 4, 6, 4, 4, 7, 4, 5, 4]  # 5 cokes
        basket_items = [BasketItem(**product_db[barcode])
                        for barcode in basket_barcodes]

        discounts = self.promotion.get_discounts(basket_items)
        discount_amounts = [discount.line_price for discount in discounts]

        assert discount_amounts == [-0.40, -0.40]

    def test_exact_multiple(self, product_db):
        """Test that the discount is calculated correctly when the number of
        eligible items is an exact multiple of m."""
        basket_barcodes = [1, 4, 6, 4, 4, 7, 4, 5, 4, 4]  # 6 cokes
        basket_items = [BasketItem(**product_db[barcode])
                        for barcode in basket_barcodes]

        discounts = self.promotion.get_discounts(basket_items)
        discount_amounts = [discount.line_price for discount in discounts]

        assert discount_amounts == [-0.40, -0.40, -0.40]


class TestMForNPoundsGroup:
    barcodes = {6, 7, 8, 9}  # Ales
    promotion = MForNPounds("3 ales for £6", barcodes, 3, 6.0)

    def test_not_exact_multiple(self, product_db):
        """Test that the discount is calculated correctly when the number of
        eligible items is not an exact multiple of m."""
        basket_barcodes = [3, 7, 1, 6, 1, 4, 4, 8, 8, 8, 2, 6, 7]
        basket_items = [BasketItem(**product_db[barcode])
                        for barcode in basket_barcodes]

        discounts = self.promotion.get_discounts(basket_items)
        discount_amounts = [discount.line_price for discount in discounts]

        # sorted eligible barcodes by price (desc): [6, 6, 7, 7, 8, 8, 8]
        # converted to prices: [2.70, 2.70, 2.55, 2.55, 2.10, 2.10, 2.10]
        # discounts = [(2.70 + 2.70 + 2.55) - 6.00, (2.55 + 2.10 + 2.10) - 6.00]
        # discounts = [1.95, 0.75]

        assert discount_amounts == [-1.95, -0.75]

    def test_exact_multiple(self, product_db):
        """Test that the discount is calculated correctly when the number of
        eligible items is an exact multiple of m."""
        basket_barcodes = [3, 7, 1, 6, 1, 4, 4, 8, 8, 8, 2, 6]
        basket_items = [BasketItem(**product_db[barcode])
                        for barcode in basket_barcodes]

        # sorted eligible barcodes by price (desc): [6, 6, 7, 8, 8, 8]
        # converted to prices: [2.70, 2.70, 2.55, 2.10, 2.10, 2.10]
        # discounts = [(2.70 + 2.70 + 2.55) - 6.00, (2.10 + 2.10 + 2.10) - 6.00]
        # discounts = [1.95, 0.30]

        discounts = self.promotion.get_discounts(basket_items)
        discount_amounts = [discount.line_price for discount in discounts]

        assert discount_amounts == [-1.95, -0.30]

    def test_not_enough_eligible_items(self, product_db):
        """Test that the discount is not applied when there are not enough
        eligible items."""
        basket_barcodes = [3, 7, 1, 6, 1, 4, 4, 2]
        basket_items = [BasketItem(**product_db[barcode])
                        for barcode in basket_barcodes]

        discounts = self.promotion.get_discounts(basket_items)
        discount_amounts = [discount.line_price for discount in discounts]

        assert discount_amounts == []

    def test_products_too_cheap(self, product_db):
        """Test that the discount is not applied if it is cheaper not to
        apply it."""
        basket_barcodes = [9, 2, 5, 9, 8]
        basket_items = [BasketItem(**product_db[barcode])
                        for barcode in basket_barcodes]

        discounts = self.promotion.get_discounts(basket_items)
        discount_amounts = [discount.line_price for discount in discounts]

        assert discount_amounts == []
