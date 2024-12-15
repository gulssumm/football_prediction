import sqlite3
import pandas as pd

# Load the CSV file into a pandas DataFrame
csv_file = "2000_01_SP_laliga.csv"  # Replace with your CSV file path
data = pd.read_csv(csv_file)

# Remove spaces from the column names
data.columns = data.columns.str.replace(' ', '_')

# Connect to SQLite database (or create it if it doesn't exist)
db_file = "spain_laliga.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the LALIGA table in the database
create_laliga_table_query = """
CREATE TABLE IF NOT EXISTS LALIGA (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    League TEXT,
    Date TEXT,
    Home_Team TEXT,
    Away_Team TEXT,
    Home_Score INTEGER,
    Away_Score INTEGER
)
"""
cursor.execute(create_laliga_table_query)

# Insert the data from the DataFrame into the LALIGA table
data.to_sql('LALIGA', conn, if_exists='append', index=False)

# Create the Users table in the database
create_users_table_query = """
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
"""
cursor.execute(create_users_table_query)

# Optional: Insert default users into the Users table
insert_users_query = """
INSERT OR IGNORE INTO Users (username, password) VALUES (?, ?)
"""
default_users = [
    ("admin", "123"),
    ("JohnDoe", "1234"),
    ("GulsumCetinozlu", "12345")
]

cursor.executemany(insert_users_query, default_users)

# Commit and close the connection
conn.commit()
conn.close()

print("Data and Users table saved successfully!")
