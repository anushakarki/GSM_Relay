import sqlite3

conn = sqlite3.connect("relay.db")
cur = conn.cursor()


# Create table for relay status
cur.execute('''CREATE TABLE IF NOT EXISTS relay_status (relay_id INTEGER PRIMARY KEY,relay_state TEXT)''')

conn.commit()
conn.close()
print("Database initialized successfully!")
