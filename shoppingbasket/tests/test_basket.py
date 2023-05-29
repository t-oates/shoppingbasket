import pytest

from shoppingbasket.basket import Basket


class TestBasket:
    def test_add_item(self):
        basket = Basket()
        basket.add_item("Beans", 0.65)
        basket.add_item("Coke", 0.70)
        assert len(basket.basket_items) == 2

    def test_add_item_from_barcode(self, products):
        basket = Basket(products=products)
        basket.add_item_from_barcode(1)
        basket.add_item_from_barcode(5)
        basket.add_item_from_barcode(5)
        assert len(basket.basket_items) == 3

    def test_add_item_from_barcode_no_product_db(self):
        basket = Basket()
        with pytest.raises(ValueError):
            basket.add_item_from_barcode(1)

    def test_add_item_from_barcode_missing(self, products):
        basket = Basket(products=products)
        with pytest.warns(UserWarning):
            basket.add_item_from_barcode(999)
