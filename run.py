import csv

PRODUCTS = {}

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

def load_orders():
  PRODUCTS = {}
  with open('orders.csv','r') as file:
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

from datetime import datetime

def write_consolidated_items_file(PRODUCTS, BUNDLES):
  PRODUCTS = load_orders()
  PRODUCTS = consolidate_bundles(PRODUCTS, BUNDLES)
  now = datetime.now()

  file = open(f"consolidated_items_{now.strftime('%m-%d-%Y')}.txt", 'w')
  file.write("Consolidated Items\n\n")
  for key in PRODUCTS:
    file.write(f"{PRODUCTS[key]} * {key}\n")

def write_orders_by_person(BUNDLES):
  now = datetime.now()
  output_file = open(f"items_by_order_{now.strftime('%m-%d-%Y')}.txt", "w")

  with open('orders.csv','r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
      order_number = row[1]
      order = row[11]
      output_file.write(f"\n{order_number}\n")
      PRODUCTS = addOrder(order, {})
      PRODUCTS = consolidate_bundles(PRODUCTS, BUNDLES)
      for key in PRODUCTS:
        output_file.write(f"{PRODUCTS[key]} * {key}\n")

BUNDLES = load_bundles('bundles.txt')

write_consolidated_items_file(PRODUCTS, BUNDLES)
write_orders_by_person(BUNDLES)