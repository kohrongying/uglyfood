import csv
import re
from sales_details import write_sales_details_file
from suppliers import write_suppliers_file
from utils import generate_csv_file_name
from os import path

"""
Takes in bundles.txt
Builds a dictionary of 
    key: Bundle Name
    value: A list of items in bundle
"""
def load_bundles(filename):
    BUNDLES = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        bundle_name = ""
        temp = []
        for line in lines:
            line = line.strip()
            if bundle_name == "":
                bundle_name = line
            else:
                if line == "":
                    BUNDLES[bundle_name] = temp
                    temp = []
                    bundle_name = ""
                else:
                    temp.append(line)
        BUNDLES[bundle_name] = temp
    return BUNDLES


def load_orders(orders_file):
    PRODUCTS = {}
    with open(orders_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            order = row[11]
            PRODUCTS = addOrder(order, PRODUCTS)
    return PRODUCTS


def addOrder(order, PRODUCTS):
    items = order.split(",")
    for item in items:
        product, qty = item.split("*")
        qty = int(qty)
        if product in PRODUCTS:
            PRODUCTS[product] += qty
        else:
            PRODUCTS[product] = qty
    return PRODUCTS

"""
Takes in the products object and bundles object
Returns consolidated items with 
    key: item name
    value: qty (integer)
"""
def consolidate_bundles(PRODUCTS, BUNDLES):
    for bundle_name in BUNDLES:
        if bundle_name in PRODUCTS:
            bundle_items = BUNDLES[bundle_name]
            bundle_qty = PRODUCTS[bundle_name]
            bundle_qty = int(bundle_qty)
            for item in bundle_items:
                if item in PRODUCTS:
                    PRODUCTS[item] += bundle_qty
                else:
                    PRODUCTS[item] = bundle_qty
            del PRODUCTS[bundle_name]
    return PRODUCTS


def write_consolidated_items_file(CONSOLIDATED):
    list_of_tuples = sorted(CONSOLIDATED.items(), key=lambda x: re.search("([A-Z])\w+", x[0]).group())

    file = open(generate_csv_file_name('consolidated_items'), 'w')
    writer = csv.writer(file)
    for tup in list_of_tuples:
        writer.writerow([tup[1], tup[0]])


POSTAL_CODES = None


def get_area(postal_code):
    if POSTAL_CODES is None:
        return ""
    else:
        if postal_code in POSTAL_CODES:
            return POSTAL_CODES[postal_code]
        else:
            return "KEY IN"


def load_postal_codes(postal_codes_file):
    file = open(postal_codes_file, 'r')
    lines = file.readlines()
    postal_codes = {}
    area = ""
    for line in lines:
        line = line.strip()
        if area == "":
            area = line
        else:
            if line == "":
                area = ""
            else:
                name, code = line.split(':')
                postal_codes[code.strip()] = area
    file.close()
    return postal_codes


def write_orders_by_person(BUNDLES, orders_file):
    output_file = open(generate_csv_file_name('items_by_order'), "w")
    writer = csv.writer(output_file)

    with open(orders_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            order_number = row[1]
            name = row[3]
            phone = row[5]
            address = row[6]
            country = row[9]
            postal_code = row[10]
            notes = ''
            if len(row) > 22:
                notes = row[22]

            writer.writerow([order_number, name])
            writer.writerow(['Address', f'{address}, {country} {postal_code}'])
            writer.writerow(['Phone number', phone])
            writer.writerow(['Customer Notes', notes])
            writer.writerow(['Area', get_area(postal_code)])

            order = row[11]
            PRODUCTS = addOrder(order, {})
            PRODUCTS = consolidate_bundles(PRODUCTS, BUNDLES)
            for key in PRODUCTS:
                writer.writerow([PRODUCTS[key], key])
            writer.writerow(['', ''])


if __name__ == '__main__':

    # File paths
    orders_file = 'orders.csv'
    suppliers_file = 'suppliers.txtt'
    bundles_file = 'bundles.txt'
    postal_codes_file = 'postal_codes.txt'

    # Common utils / helpers
    BUNDLES = load_bundles(bundles_file)
    PRODUCTS = load_orders(orders_file)
    CONSOLIDATED = consolidate_bundles(PRODUCTS, BUNDLES)
    if path.exists(postal_codes_file):
        POSTAL_CODES = load_postal_codes(postal_codes_file)

    # write CSV calls
    write_consolidated_items_file(CONSOLIDATED)
    write_orders_by_person(BUNDLES, orders_file)
    # write_sales_details_file(orders_file)
    # if path.exists(suppliers_file):
    #     write_suppliers_file(CONSOLIDATED, suppliers_file)
    print("Completed! Consolidated items and items by order csv files generated!")
