# shoppingbasket
shoppingbasket is a simple Python package to track items in a shopping basket and generate an invoice/receipt based on these items and applied promotions.

## Requirements
Requires Python >= 3.10.

Install requirements using either [environment.yml](environment.yml) or [requirements.txt](requirements.txt):

`conda env create --file=environment.yml` or `pip install -r requirements.txt`

## Examples

### Quickstart
A basic shopping basket can be initialised empty, and then items added to it manually.

https://github.com/timbonator/shoppingbasket/blob/5c6e936f2a3829748e360787a459f3d7191c90da/shoppingbasket/examples/quickstart.py#L1-L13

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

https://github.com/timbonator/shoppingbasket/blob/db5c14d3798066ee98981aef12d8df6d1a8750df/shoppingbasket/examples/using_product_db.py#L1-L18

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

https://github.com/timbonator/shoppingbasket/blob/db5c14d3798066ee98981aef12d8df6d1a8750df/shoppingbasket/examples/using_product_db.py#L22-L32

**Example YAML file**:
https://github.com/timbonator/shoppingbasket/blob/946d1060fdcbca2a1f312fbb603ab97bd6f71f31/shoppingbasket/examples/data/products.yaml#L1-L38

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

https://github.com/timbonator/shoppingbasket/blob/946d1060fdcbca2a1f312fbb603ab97bd6f71f31/shoppingbasket/examples/with_promotions.py#L6-L19

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

https://github.com/timbonator/shoppingbasket/blob/8270285a781e2d362d659041dcc0f3986c3572d7/shoppingbasket/examples/with_promotions.py#L3-L19

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
