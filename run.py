import csv
import re
from sales_details import write_sales_details_file
from utils import generate_csv_file_name


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


def write_consolidated_items_file(BUNDLES, orders_file):
    PRODUCTS = load_orders(orders_file)
    PRODUCTS = consolidate_bundles(PRODUCTS, BUNDLES)
    list_of_tuples = sorted(PRODUCTS.items(), key=lambda x: re.search("([A-Z])\w+", x[0]).group())

    file = open(generate_csv_file_name('consolidated_items'), 'w')
    writer = csv.writer(file)
    for tup in list_of_tuples:
        writer.writerow([tup[1], tup[0]])


def write_orders_by_person(BUNDLES, orders_file):
    output_file = open(generate_csv_file_name('items_by_order'), "w")
    writer = csv.writer(output_file)

    with open(orders_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            order_number = row[1]
            name = row[3]
            writer.writerow([order_number, name])

            order = row[11]
            PRODUCTS = addOrder(order, {})
            PRODUCTS = consolidate_bundles(PRODUCTS, BUNDLES)
            for key in PRODUCTS:
                writer.writerow([PRODUCTS[key], key])
            writer.writerow(['', ''])


if __name__ == '__main__':
    orders_file = 'orders.csv'
    BUNDLES = load_bundles('bundles.txt')
    write_consolidated_items_file(BUNDLES, orders_file)
    write_orders_by_person(BUNDLES, orders_file)
    write_sales_details_file(orders_file)
    print("Completed! Consolidated items and items by order csv files generated!")
