import pytest

from shoppingbasket.basket_item import BasketItem, Discount


class TestBasketItem:
    basket_items = {
        'Beans': BasketItem('Beans', 0.5),
        'Onions': BasketItem('Onions', 1.99, units='kg', quantity=2.569)
    }

    @pytest.mark.parametrize(
        'item_name, expected_line_price',
        [('Beans', 0.5), ('Onions', 5.11)]
    )
    def test_line_price(self, item_name, expected_line_price):
        assert self.basket_items[item_name].line_price == expected_line_price

    @pytest.mark.parametrize(
        'item_name, num_desc_lines',
        [('Beans', 1), ('Onions', 2)]
    )
    def test_description(self, item_name, num_desc_lines):
        """Test that description has two lines if item has units."""
        basket_item = self.basket_items[item_name]
        assert len(basket_item.description.splitlines()) == num_desc_lines


class TestDiscount:
    discount = Discount('Beans 3 for 2', 0.5)

    def test_line_price(self):
        """Test that the line price of a discount is negative."""
        assert self.discount.line_price == -0.5
