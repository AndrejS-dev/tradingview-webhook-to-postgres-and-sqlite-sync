import psycopg2
import sqlite3
from datetime import datetime
import logging
import decimal

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Neon PostgreSQL connection details (replace with your credentials)
NEON_DB = {
    "dbname": "",
    "user": "",
    "password": "",
    "host": "",
    "port": ""
}

# Local SQLite file
LOCAL_DB = "local.db"

# Define table mappings (Neon table name, Local SQLite table name)
# Updated based on your error output (e.g., webhook_btcusd_1h)
TABLE_MAPPINGS = [
    ("webhook_btcusd_1h", "BTCUSD_1H"),
    ("webhook_ethusd_1h", "ETHUSD_1H"),
    ("webhook_solusd_1h", "SOLUSD_1H"),
    ("webhook_xrpusd_1h", "XRPUSD_1H"),
    ("webhook_bnbusd_1h", "BNBUSD_1H"),
    ("webhook_suiusd_1h", "SUIUSD_1H"),
    # If you have more tables, add more tuples (NEON_DB_table_name, LocalDB_table_name)
]

# Register SQLite adapters and converters for datetime
def adapt_datetime(dt):
    return dt.isoformat()

def convert_datetime(s):
    return datetime.fromisoformat(s.decode('utf-8'))

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("time", convert_datetime)

def setup_local_db():
    """Set up the local SQLite database with the specified table names."""
    conn = sqlite3.connect(LOCAL_DB, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    for _, local_table in TABLE_MAPPINGS:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {local_table} (
                id INTEGER PRIMARY KEY,
                time TIME,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL
            )
        """)
        # Add an index on time for faster queries
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{local_table}_time ON {local_table} (time)")

    conn.commit()
    conn.close()

def setup_sync_tracker():
    """Create a table to track the last sync time for each local table."""
    conn = sqlite3.connect(LOCAL_DB, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_tracker (
            table_name TEXT PRIMARY KEY,
            last_sync_time TEXT
        )
    """)
    # Initialize last sync time for each local table
    for _, local_table in TABLE_MAPPINGS:
        cursor.execute("""
            INSERT OR IGNORE INTO sync_tracker (table_name, last_sync_time)
            VALUES (?, ?)
        """, (local_table.lower(), "1970-01-01 00:00:00+00:00"))
    conn.commit()
    conn.close()

def get_last_sync_time(local_table_name):
    """Get the last sync time for a given local table."""
    conn = sqlite3.connect(LOCAL_DB, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    cursor.execute("SELECT last_sync_time FROM sync_tracker WHERE table_name = ?", (local_table_name.lower(),))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "1970-01-01 00:00:00+00:00"

def update_last_sync_time(local_table_name, time):
    """Update the last sync time for a given local table."""
    conn = sqlite3.connect(LOCAL_DB, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO sync_tracker (table_name, last_sync_time)
        VALUES (?, ?)
    """, (local_table_name.lower(), time.isoformat() if isinstance(time, datetime) else time))
    conn.commit()
    conn.close()

def sync_databases():
    # Set up local database and sync tracker
    setup_local_db()
    setup_sync_tracker()

    # Connect to Neon PostgreSQL
    try:
        neon_conn = psycopg2.connect(**NEON_DB)
        neon_cursor = neon_conn.cursor()
    except psycopg2.Error as e:
        logger.error(f"Failed to connect to Neon: {e}")
        return

    # Connect to local SQLite
    sqlite_conn = sqlite3.connect(LOCAL_DB, detect_types=sqlite3.PARSE_DECLTYPES)
    sqlite_cursor = sqlite_conn.cursor()

    for neon_table, local_table in TABLE_MAPPINGS:
        logger.info(f"Syncing Neon table {neon_table} to local table {local_table}...")
        last_sync = get_last_sync_time(local_table)

        # Fetch new records from Neon
        query = f"""
            SELECT id, time, open, high, low, close, volume
            FROM {neon_table}
            WHERE time > %s
            ORDER BY time ASC
        """
        try:
            neon_cursor.execute(query, (last_sync,))
            new_records = neon_cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error fetching from Neon for {neon_table}: {e}")
            continue

        if new_records:
            logger.info(f"Found {len(new_records)} new records for {neon_table}.")
            # Convert decimal.Decimal to float for SQLite compatibility
            converted_records = [
                (rec[0], rec[1], float(rec[2]), float(rec[3]), float(rec[4]), float(rec[5]), float(rec[6]))
                for rec in new_records
            ]
            # Update local SQLite
            sqlite_cursor.executemany(f"""
                INSERT OR REPLACE INTO {local_table} (id, time, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, converted_records)
            sqlite_conn.commit()

            # Update the last sync time
            latest_time = new_records[-1][1]  # time is the 2nd column
            update_last_sync_time(local_table, latest_time)
        else:
            logger.info(f"No new records for {neon_table}.")

    # Clean up
    neon_cursor.close()
    neon_conn.close()
    sqlite_cursor.close()
    sqlite_conn.close()

if __name__ == "__main__":
    logger.info("Syncing databases...")
    sync_databases()
