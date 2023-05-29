from shoppingbasket import Basket

basket = Basket()

# Items have names and prices
basket.add_item("Beans", 0.65)
basket.add_item("Coke", 0.70)

# Add item that is measure in specific units
basket.add_item("Onions", 0.50, units="kg", quantity=0.5)

# print receipt
print(basket.generate_invoice().to_string())
