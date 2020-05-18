# Supplier qty (csv)
# According to supplier
# Qty of each item goods

# Load suppliers by item. { item: { supplier, qty } }
import csv

from utils import generate_csv_file_name

"""
Returns CSV of Supplier
By Supplier
Item name, Quantity needed
Item name, Quantity needed
"""
def write_suppliers_file(consolidated, suppliers_file):
    supply = load_suppliers_file(suppliers_file)

    # Updates supply object with customer quantity
    for item, qty in consolidated.items():
        if item in supply:
            supply[item]['qty'] += qty
        else:
            print(f'ERROR: {item} not found in supplier.txt')

    # Sort supply by supplier
    supply = sort_supply(supply)

    # Write to csv
    write_file = open(generate_csv_file_name('supplier_qty'), 'w')
    writer = csv.writer(write_file)
    for supplier in supply:
        writer.writerow([supplier])
        products = supply[supplier]
        for product in products:
            writer.writerow([product['product'], product['qty']])
        writer.writerow([])


"""
Loads the suppliers.txt file and builds a supply dictionary object
"""
def load_suppliers_file(suppliers_file):
    file = open(suppliers_file, 'r')
    lines = file.readlines()
    return build_supply(lines)

"""
Builds a supply object where:
    key: Name of supply
    value: { supplier: <name>, qty: 0 }
"""
def build_supply(lines):
    SUPPLY = {}
    current_state = 'START'
    supplier_name = ''
    for line in lines:
        line = line.strip()
        if current_state == 'START':
            if line:
                supplier_name = line
                current_state = 'NAME'
        elif current_state == 'NAME':
            if line:
                SUPPLY[line] = {"supplier": supplier_name, 'qty': 0}
            else:
                current_state = 'START'
    return SUPPLY

"""
Takes in SUPPLY dictionary and maps it to another dictionary where
    key is Supplier
    value is a list of objects with supply and quantity
"""
def sort_supply(supply):
    sort_by_supplier = {}
    for product in supply:
        supplier = supply[product]['supplier']
        if supplier in sort_by_supplier:
            sort_by_supplier[supplier].append({
                'product': product,
                'qty': supply[product]['qty']
            })
        else:
            sort_by_supplier[supplier] = [{
                'product': product,
                'qty': supply[product]['qty']
            }]
    return sort_by_supplier
