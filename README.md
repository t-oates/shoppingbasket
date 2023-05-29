# ShoppingBasket
ShoppingBasket is a simple Python package to track items in a shopping basket and generate an invoice/receipt based on these items and applied promotions.

## The Task
The task is to model a supermarket pricing calculator in software. This is inspired by PragDave’s Supermarket Kata.

You should write a program which works out how to price a shopping basket, allowing for different pricing structures including:

 - Three tins of beans for the price of two
 - Onions for 29p / kg
 - Two cans of coca-cola for £1
 - Any 3 ales from the set {…} for £6

Here’s an example of a receipt illustrating the type of output that should be possible (although your program doesn’t need to produce nicely formatted output like this):
Item               | Price
-------------------| -------------
Beans              | 0.50
Beans              | 0.50
Beans              | 0.50
Coke               | 0.70
Coke               | 0.70
Oranges            |
0.200kg @ £1.99/kg | 0.40
**Sub-total**      | 3.30
**Savings**        |
Beans 3 for 2      | -0.50
Coke 2 for £1      | -0.40
**Total savings**  | -0.90
**Total to Pay**   | -2.40
 
We’d like you to do your work under version control (preferably using git) and provide us with a copy of the repository when you have finished (by showing us a GitHub / similar repository, or sending us a zip of the repository if you prefer).

Your work does not need to account for user interface or IO; we are interested in how you represent a basket of things and a set of pricing rules, how you compute the correct price for the basket, and what you have done to assess the correctness of what you have made.

You should be designing with some thought to how the requirements might change and assessing the ways they are incomplete.

We would also like the repository to contain a README explaining what you have done, how to use your work, and any trade-offs, limitations or particularly excellent features of what you have made.

We would prefer if you use some of the technologies we are most familiar with, so ideally this would be written in one of Python, Clojure, Java or Javascript. We understand that we’re asking you to do work in your free time and that this might be hard to accommodate, so please do not feel you have to spend ages on it.

## Examples

### Quickstart
A basic shopping basket can be initialised empty, and then items added to it manually.

https://github.com/timbonator/shoppingbasket/blob/37843014cb2095d032b3d71cf8b11bf8e2c301c9/shoppingbasket/examples/quickstart.py

Output:
```
Item                    Price
=============================
Beans                   £0.65
Coke                    £0.70
Onions                       
0.5kg @ £0.5/kg         £0.25
--------------------   ------
Sub-total               £1.60
--------------------   ------
Total to pay            £1.60
```

### Using ProductDB
Instead of manually entering a product each time, the basket can be initialised with a database, and then project retrieved by barcode.

https://github.com/timbonator/shoppingbasket/blob/4a6cbb688626659c0072915a4fc849dce7c50d59/shoppingbasket/examples/using_product_db.py

#### Reading a YAML file
A nice way of setting up your products database is by importing the data from a YAML file:

https://github.com/timbonator/shoppingbasket/blob/ccd3ff9c45c9753a58b705a2770b45d450a6330f/shoppingbasket/examples/from_yaml.py

YAML file:
https://github.com/timbonator/shoppingbasket/blob/ccd3ff9c45c9753a58b705a2770b45d450a6330f/shoppingbasket/examples/data/products.yaml

Output:
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

https://github.com/timbonator/shoppingbasket/blob/bab543d4b3f9263ac966cad158ff1f7b98c016d8/shoppingbasket/examples/with_promotions.py

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
Generating an invoice to match the example one in the task spec:

https://github.com/timbonator/shoppingbasket/blob/493f07e6595fd7c3e54c287ea9461ce33188ec69/shoppingbasket/examples/from_task_spec.py

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
