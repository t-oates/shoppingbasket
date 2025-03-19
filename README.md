# shoppingbasket
shoppingbasket is a simple Python package to track items in a shopping basket and generate an invoice/receipt based on these items and applied promotions.

## Requirements
Requires Python >= 3.10.

Install requirements using either [environment.yml](environment.yml) or [requirements.txt](requirements.txt):

`conda env create --file=environment.yml` or `pip install -r requirements.txt`

## Examples

### Quickstart
A basic shopping basket can be initialised empty, and then items added to it manually.

```python
from shoppingbasket import Basket

basket = Basket()

# Items have names and prices
basket.add_item("Beans", 0.65)
basket.add_item("Coke", 0.70)

# Add item that is measure in specific units
basket.add_item("Onions", 0.50, units="kg", quantity=0.5)

# print receipt
print(basket.generate_invoice().to_string())
```

**Output:**
```
Item                    Price
=============================
Beans                   £0.65
Coke                    £0.70
Onions                       
0.5kg @ £1.0/kg         £0.50
--------------------   ------
Sub-total               £1.85
--------------------   ------
Total to pay            £1.85
```

### Using ProductDB
Instead of manually entering a product each time, the basket can be initialised with a database, and then project retrieved by barcode.

```python
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
```

**Output:**
```
Item                    Price
=============================
Beans                   £1.50
Onions                       
0.5kg @ £0.29/kg        £0.14
Coke                    £0.70
Beans                   £1.50
--------------------   ------
Sub-total               £3.84
--------------------   ------
Total to pay            £3.84
```

#### Reading a YAML file
A nice way of setting up your products database is by importing the data from a YAML file:

```python
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
```

**Example YAML file**:
```
- barcode: 1
  name: Beans
  unit_price: 0.50

- barcode: 2
  name: Onions
  unit_price: 0.29
  units: kg

- barcode: 3
  name: Bananas
  unit_price: 0.11
  units: kg

- barcode: 4
  name: Coke
  unit_price: 0.70

- barcode: 5
  name: Oranges
  unit_price: 1.99
  units: kg

- barcode: 6
  name: CSE Finest Ale
  unit_price: 2.70

- barcode: 7
  name: Tim's Ale
  unit_price: 2.55

- barcode: 8
  name: Value IPA
  unit_price: 2.10

- barcode: 9
  name: Super Value IPA
  unit_price: 1.10
```

**Output:**
```
Item                    Price
=============================
Beans                   £0.50
Beans                   £0.50
Oranges                      
0.2kg @ £1.99/kg        £0.40
Coke                    £0.70
Coke                    £0.70
--------------------   ------
Sub-total               £2.80
--------------------   ------
Total to pay            £2.80
```

## Promotions
Discounts can be applied using two different Promotions models:
 - `MForN`: Buy M products (of the same type) and pay the price of N.
 - `MForNPounds`: Buy M products in a set of products and pay N pounds (these can be different products).

```python
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
```

Output:
```
Item                    Price
=============================
Beans                   £0.50
Tim's Ale               £2.55
CSE Finest Ale          £2.70
Value IPA               £2.10
CSE Finest Ale          £2.70
Beans                   £0.50
--------------------   ------
Sub-total              £11.05
--------------------   ------
Savings                      
--------------------   ------
3 ales for £6          £-1.95
--------------------   ------
Total savings          £-1.95
--------------------   ------
Total to pay            £9.10
```

## Example from the task spec
Generating an invoice to match the example from the task spec, sent via email:

```python
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
```

Output:
```
Item                    Price
=============================
Beans                   £0.50
Beans                   £0.50
Beans                   £0.50
Coke                    £0.70
Coke                    £0.70
Oranges                      
0.2kg @ £1.99/kg        £0.40
--------------------   ------
Sub-total               £3.30
--------------------   ------
Savings                      
--------------------   ------
Beans 3 for 2          £-0.50
Coke 2 for £1          £-0.40
--------------------   ------
Total savings          £-0.90
--------------------   ------
Total to pay            £2.40
```

# Limitations
There are a few limitations and potential improvements that could be made to the software. Many are listed [in the repository's issues](https://github.com/timbonator/shoppingbasket/issues).

These are the ones that stand out to me the most:
1) Currently, there is **no logic to detect whether an item belongs to multiple promotions**. This means that discounts might be applied too many times. Discounts should (unless otherwise specified) be calculated based on which combination gives the greatest total discount, without a single item being used multiple times.
2) The **product database must either be created from a YAML file or manually**. It would be nice to have features to read from CSV, JSON, SQL, etc.
3) **Promotion creation is not very user-friendly**. It would be nice to have a way to import them from file (in case of lots of discounts) or enter them from the command prompt.
4) **Only two types of promotion**: New types of promotion can easily be created in future by inheriting from Promotion (only the 'get_discounts' method needs to be define), but there is no way with the current software to create a promotion that doesn't either fit under "N items for the price of M" or "N items for £M". Additionally, MForN cannot be applied to groups of different types of items.
