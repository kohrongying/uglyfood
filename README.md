# Uglyfood

- Consolidate orders by person
- Consolidate orders by sales item (NEW: Include address, contact number and area)
- (NEW) Get sales details
- (NEW) Consolidate supply by supplier

### Dependencies: 
- Python3

### Required files
* `orders.csv`
* `bundles.txt` 
    - Update bundle information
    - Leave one empty line between each bundle
* `suppliers.txt`
    - Update supplier and their goods information
    - Leave one empty line between each supplier
* `postal_codes.txt`
    - Update customer postal codes
    - Leave one empty line between each area
    - Use format: <name>: <postal_code>

### How to run
1. Run `python run.py` or `python3 run.py`


Note: Sorting happens as it takes the first capital letter of the item. 
