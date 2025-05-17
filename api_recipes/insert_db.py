import sqlite3


def insert_data(db_name, table_name, data):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    """
    )

    # Insert data into the table
    cursor.executemany(f"INSERT INTO {table_name} (name, age) VALUES (?, ?)", data)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
