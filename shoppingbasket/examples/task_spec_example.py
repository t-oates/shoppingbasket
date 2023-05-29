from shoppingbasket import ProductDB, Basket
from shoppingbasket.promotions import MForN, MForNPounds

# Setup basket with product database
products = ProductDB.from_yaml('data/products.yaml')
basket = Basket(products=products)

# Add items
basket.add_item_from_barcode(1)
basket.add_item_from_barcode(1)
basket.add_item_from_barcode(1)
basket.add_item_from_barcode(4)
basket.add_item_from_barcode(4)
basket.add_item_from_barcode(5, 0.2)

# Produce invoice with promotions
promotions = [
    MForN("Beans 3 for 2", {1}, m=3, n=2),
    MForNPounds("Coke 2 for £1", {4}, m=2, n=1.0),
]

invoice = basket.generate_invoice(promotions=promotions)
print(invoice.to_string())
