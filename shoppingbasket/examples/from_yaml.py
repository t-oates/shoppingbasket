from shoppingbasket import ProductDB, Basket

import os
print(os.getcwd())

yaml_path = 'data/products.yaml'
product_db = ProductDB.from_yaml(yaml_path)

basket = Basket(products=product_db)
basket.add_item_from_barcode(1)
basket.add_item_from_barcode(1)
basket.add_item_from_barcode(5, 0.2)
basket.add_item_from_barcode(4)
basket.add_item_from_barcode(4)

print(basket.generate_invoice().to_string())
