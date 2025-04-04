import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

# Drop and recreate food table
cur.execute("DROP TABLE IF EXISTS food")
cur.execute('''
    CREATE TABLE food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        packets INTEGER,
        amount TEXT,
        location TEXT,
        claimed INTEGER DEFAULT 0
    )
''')

# Create users table
cur.execute("DROP TABLE IF EXISTS users")
cur.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')

con.commit()
con.close()
print("Database reset and created with users table.")
