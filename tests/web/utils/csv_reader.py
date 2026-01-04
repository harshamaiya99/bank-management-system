import csv

def read_csv_data(file_path):
    """Reads CSV and returns a list of dictionaries"""
    with open(file_path, newline="") as csvfile:
        return list(csv.DictReader(csvfile))