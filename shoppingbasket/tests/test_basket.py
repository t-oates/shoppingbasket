import pytest

from shoppingbasket.basket import Basket
from shoppingbasket import Invoice
from shoppingbasket.basket_item import BasketItem
from shoppingbasket.promotions import MForN, MForNPounds


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


class TestInvoice:
    basket_items = [
        BasketItem("Beans", 0.65, barcode=1),
        BasketItem("Coke", 0.70, barcode=5),
        BasketItem("Beans", 0.65, barcode=1),
        BasketItem("Beans", 0.65, barcode=1),
        BasketItem("Coke", 0.70, barcode=5),
        BasketItem("Beans", 0.65, barcode=1),
        BasketItem("Beans", 0.65, barcode=1),
        BasketItem("Beans", 0.65, barcode=1),
        BasketItem("Carrots", 1.00, barcode=2, units="kg", quantity=0.5),
    ]
    promotions = [
        MForN("Beans 3 for 2", {1}, m=3, n=2),
        MForNPounds("Coke 2 for £1", {5}, m=2, n=1.0),
    ]
    invoice = Invoice(basket_items, promotions)
    invoice_without_promotions = Invoice(basket_items)

    def test_get_discounts(self):
        assert len(self.invoice.discounts) == 3
        assert len(self.invoice_without_promotions.discounts) == 0

    def test_subtotal(self):
        assert self.invoice.subtotal == 5.80
        assert self.invoice_without_promotions.subtotal == 5.80

    def test_discount_total(self):
        assert self.invoice.discount_total == -1.70
        assert self.invoice_without_promotions.discount_total == 0.0

    def test_total(self):
        assert self.invoice.total == 4.10
        assert self.invoice_without_promotions.total == 5.80

    def test_to_string(self):
        with_promos_str = self.invoice.to_string()
        without_promos_str = self.invoice_without_promotions.to_string()

        assert with_promos_str.count("Beans") == 8
        assert without_promos_str.count("Beans") == 6
        assert "Savings" in with_promos_str
        assert "Savings" not in without_promos_str

    def test_no_promos_applicable(self):
        basket_items = [
            BasketItem("Coke", 0.70, barcode=5),
            BasketItem("Beans", 0.65, barcode=1),
            BasketItem("Beans", 0.65, barcode=1),
            BasketItem("Carrots", 1.00, barcode=2, units="kg", quantity=0.5),
        ]
        invoice = Invoice(basket_items, self.promotions)
        assert len(invoice.discounts) == 0
