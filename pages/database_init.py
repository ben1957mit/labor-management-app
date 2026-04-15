# database_init.py

import sqlite3

DB_FILE = "daily_cost_records.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ---------------------------------------------------
    # RECORDS TABLE
    # ---------------------------------------------------
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

    # ---------------------------------------------------
    # SITES TABLE
    # ---------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sites (
        SiteName TEXT PRIMARY KEY
    )
    """)

    # ---------------------------------------------------
    # COST CATEGORIES TABLE
    # ---------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cost_categories (
        CategoryName TEXT PRIMARY KEY
    )
    """)

    # ---------------------------------------------------
    # DEFAULT COST CATEGORIES (ONLY IF MISSING)
    # ---------------------------------------------------
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


   
