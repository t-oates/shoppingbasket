import pytest

from till import TillItem


class TestTillItemPerItem:
    items = {1: TillItem(1, 'Beans', 0.5),
             2: TillItem(2, 'Onions', 1.99, 'kg', 2.569)}

    # 5.11 = 1.99 * 2.569 (rounded to 2dp)
    @pytest.mark.parametrize('barcode, price', [(1, 0.5), (2, 5.11)])
    def test_price(self, barcode, price):
        assert self.items[barcode].price == price

    @pytest.mark.parametrize('barcode, price_gbp, num_lines',
                             [(1, '£0.50', 1), (2, '£5.11', 2)])
    def test_to_receipt_string(self, barcode, price_gbp, num_lines):
        receipt_string = self.items[barcode].to_receipt_string()
        assert price_gbp in receipt_string
        assert len(receipt_string.splitlines()) == num_lines
