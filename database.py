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

# Create the table in the database
create_table_query = """
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
cursor.execute(create_table_query)

# Insert the data from the DataFrame into the database
data.to_sql('LALIGA', conn, if_exists='append', index=False)

# Commit and close the connection
conn.commit()
conn.close()

print("Data saved successfully!")
