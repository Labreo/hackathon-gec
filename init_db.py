import sqlite3
#Dont run this again pls.
# Connect to SQLite database (or create it)
conn = sqlite3.connect('pickups.db')
cursor = conn.cursor()

# Create 'users' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    address TEXT NOT NULL,
    age INTEGER NOT NULL,
    sex TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

#Create pickup table
cursor.execute('''
CREATE TABLE IF NOT EXISTS pickups (
    user_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    waste_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending', 
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')


conn.commit()
conn.close()
print("Database and users table created.")
