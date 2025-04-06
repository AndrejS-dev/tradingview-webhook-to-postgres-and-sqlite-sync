import sqlite3

def fetch_data(db_path, table_name):
# Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all data from the specified table
    query = f"SELECT * FROM {table_name};"
    cursor.execute(query)

    # Retrieve column names
    columns = [desc[0] for desc in cursor.description]

    # Fetch all rows
    rows = cursor.fetchall()

    # Transpose rows to columns
    column_data = {col: [] for col in columns}
    for row in rows:
        for col, value in zip(columns, row):
            column_data[col].append(value)

    # Close the connection
    conn.close()

    return column_data

# Example usage
db_path = "local.db"
table_name = "BTCUSD_1H"
data = fetch_data(db_path, table_name)

# Access specific columns as lists
dates = data.get("time", []) 
prices = data.get("close", [])

for index, price in enumerate(prices):
    print(f"Time: {dates[index]} | {price}")