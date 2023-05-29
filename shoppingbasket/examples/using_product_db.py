from shoppingbasket import ProductDB, Basket

# Create basket with a products database
products = ProductDB([
    {'barcode': 1, 'name': 'Beans', 'unit_price': 1.5},
    {'barcode': 2, 'name': 'Coke', 'unit_price': 0.70},
    {'barcode': 3, 'name': 'Onions', 'unit_price': 0.29, 'units': 'kg'},
])
basket = Basket(products=products)

# Add items to basket using barcode
basket.add_item_from_barcode(1)
basket.add_item_from_barcode(3, 0.5)
basket.add_item_from_barcode(2)
basket.add_item_from_barcode(1)

# Same output as above
print(basket.generate_invoice().to_string())
