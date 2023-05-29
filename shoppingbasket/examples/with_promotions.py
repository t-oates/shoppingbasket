from shoppingbasket import promotions, Basket, ProductDB

yaml_path = 'data/products.yaml'
product_db = ProductDB.from_yaml(yaml_path)

basket = Basket(products=product_db)
basket.add_item_from_barcode(1)
basket.add_item_from_barcode(7)
basket.add_item_from_barcode(6)
basket.add_item_from_barcode(8)
basket.add_item_from_barcode(6)
basket.add_item_from_barcode(1)

promotions = [
    promotions.MForN("Beans 3 for 2", {1}, m=3, n=2),
    promotions.MForNPounds("3 ales for £6", {6, 7, 8, 9}, m=3, n=6.0)
]

invoice = basket.generate_invoice(promotions=promotions)
print(invoice.to_string())
