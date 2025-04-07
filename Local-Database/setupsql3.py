import sqlite3

# Local SQLite file
LOCAL_DB = "local.db"

def setup_local_db():
    conn = sqlite3.connect(LOCAL_DB)
    cursor = conn.cursor()

    # Create a table for each a asset
    tables = [
        "BTCUSD_1H", "ETHUSD_1H", "SOLUSD_1H", "XRPUSD_1H", "BNBUSD_1H", "SUIUSD_1H",
        # If you want more tables, put the names for them in the list and run the script
        # The tables already created will not be changed when running the script again
    ]

    for table in tables:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY,
                time TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL
            )
        """)
        # Add an index on timestamp for faster queries
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table}_time ON {table} (time)")

    conn.commit()
    conn.close()

# Run setup
setup_local_db()