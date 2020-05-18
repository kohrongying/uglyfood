
from datetime import datetime


def generate_csv_file_name(name):
    return f"{name}_{datetime.now().strftime('%m-%d-%Y')}.csv"