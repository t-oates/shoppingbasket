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
basket.add_item_from_barcode(3, quantity=0.5)  # A product that has units
basket.add_item_from_barcode(2)
basket.add_item_from_barcode(1)

invoice = basket.generate_invoice()
print(invoice.to_string())


# Crate basket with a products database from yaml file
yaml_path = 'data/products.yaml'
product_db_yaml = ProductDB.from_yaml(yaml_path)

basket_yaml = Basket(products=product_db_yaml)
basket_yaml.add_item_from_barcode(1)
basket_yaml.add_item_from_barcode(1)
basket_yaml.add_item_from_barcode(5, quantity=0.2)
basket_yaml.add_item_from_barcode(4)
basket_yaml.add_item_from_barcode(4)

invoice_yaml = basket_yaml.generate_invoice()
print(invoice_yaml.to_string())
