import pytest

from basket import BasketItem


class TestBasketItem:
    @pytest.mark.parametrize(
        'basket_item, expected_price', [
            (BasketItem('Beans', 0.5), 0.5),
            # 5.11 = 1.99 * 2.569 (rounded to 2dp)
            (BasketItem('Onions', 1.99, units='kg', amount=2.569), 5.11),
        ]
    )
    def test_price(self, basket_item, expected_price):
        assert basket_item.price == expected_price
