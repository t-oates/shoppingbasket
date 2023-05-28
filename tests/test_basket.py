import pytest

from product_db import Product
from basket import BasketItem


class TestBasketItem:
    basket_items = {
        1: BasketItem(Product(1, 'Beans', 0.5, 'per_item')),
        2: BasketItem(Product(2, 'Onions', 1.99, 'kg'), 2.569),
    }

    # 5.11 = 1.99 * 2.569 (rounded to 2dp)
    @pytest.mark.parametrize('barcode, price', [(1, 0.5), (2, 5.11)])
    def test_price(self, barcode, price):
        assert self.basket_items[barcode].price == price

    @pytest.mark.parametrize('barcode, price, num_lines',
                             [(1, 0.50, 1), (2, 5.11, 2)])
    def test_to_receipt_line(self, barcode, price, num_lines):
        receipt_line = self.basket_items[barcode].to_receipt_line()
        assert receipt_line.price == price
        assert len(receipt_line.description.splitlines()) == num_lines
