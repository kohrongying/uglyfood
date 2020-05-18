# Supplier qty (csv)
# According to supplier
# Qty of each item goods

# Load suppliers by item. { item: { supplier, qty } }


def write_suppliers_file(orders_file, suppliers_file):
    SUPPLIERS = load_suppliers_file(suppliers_file)


def load_suppliers_file(suppliers_file):
    return