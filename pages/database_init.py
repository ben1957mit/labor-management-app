# database_init.py

import sqlite3

DB_FILE = "daily_cost_records.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Records table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        Timestamp TEXT,
        Date TEXT,
        Shift TEXT,
        UnitsProduced REAL,
        OrdersProcessed REAL,
        LaborHours REAL,
        Data JSON,
        Site TEXT
    )
    """)

    # Sites table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sites (
        SiteName TEXT PRIMARY KEY
    )
    """)

    # Cost categories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cost_categories (
        CategoryName TEXT PRIMARY KEY
    )
    """)

    # Default categories (only inserted if missing)
    cursor.executemany(
        "INSERT OR IGNORE INTO cost_categories VALUES (?)",
        [
            ("Labor",),
            ("Equipment",),
            ("Supplies",),
            ("Transportation",),
            ("Admin",)
        ]
    )

    conn.commit()
    return conn, cursor
