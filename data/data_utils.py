import os
import csv
from datetime import datetime

DATA_DIR = "data"

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def csv_path(filename: str) -> str:
    ensure_data_dir()
    return os.path.join(DATA_DIR, filename)

def append_row(filename: str, fieldnames: list, row: dict):
    path = csv_path(filename)
    file_exists = os.path.isfile(path)

    with open(path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def read_rows(filename: str) -> list:
    path = csv_path(filename)
    if not os.path.isfile(path):
        return []
    with open(path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")
