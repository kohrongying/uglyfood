import csv
from utils import generate_csv_file_name


def write_sales_details_file(orders_file):
    total_discount = 0
    total_sales = 0
    total_num_orders = 0
    COUPONS = {}

    # Read orders csv
    with open(orders_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            COUPONS = set_coupon(COUPONS, row)
            total_discount += get_discount(row)
            total_sales += get_total(row)
            total_num_orders += 1

    # Write to csv
    write_file = open(generate_csv_file_name('sales_generated'), 'w')
    writer = csv.writer(write_file)
    writer.writerow(["Total Discount", total_discount])
    writer.writerow(['Total Sales', total_sales])
    writer.writerow(['Total Number of Orders', total_num_orders])
    writer.writerow([])
    writer.writerow(['Coupons used'])
    for coupon in COUPONS:
        writer.writerow([coupon, COUPONS[coupon]])


def get_subtotal(row):
    subtotal = row[13]
    if subtotal[0] == '$':
        subtotal = subtotal[1:]
        subtotal = float(subtotal)
    else:
        raise Exception('Invalid Subtotal')
    return subtotal


def get_total(row):
    total = row[19]
    if total[0] == '$':
        total = total[1:]
        total = float(total)
    else:
        raise Exception('Invalid Total')
    return total


def get_discount(row):
    discount = row[16]
    if discount[0] == '$':
        discount = discount[1:]
        discount = float(discount)
    else:
        raise Exception('Invalid Total')
    return discount


def set_coupon(COUPONS, row):
    coupon_code = row[15]
    if coupon_code:
        if coupon_code in COUPONS:
            COUPONS[coupon_code] += 1
        else:
            COUPONS[coupon_code] = 1
    return COUPONS
