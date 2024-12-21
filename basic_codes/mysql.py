import mysql.connector
import pandas as pd

# Load the CSV file into a pandas DataFrame
csv_file = "2000_01_SP_laliga.csv"  # Replace with your CSV file path
data = pd.read_csv(csv_file)

# Connect to MySQL database
db_config = {
    'host': 'localhost',  # MySQL host (use 'localhost' if running locally)
    'user': 'root',       # Your MySQL username
    'password': 'your_password',  # Your MySQL password
    'database': 'football_db'  # Your MySQL database name
}

try:
    # Establish connection to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create the table in the database if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS laliga_matches (
        id INT AUTO_INCREMENT PRIMARY KEY,
        League VARCHAR(255),
        Date VARCHAR(255),
        Home_Team VARCHAR(255),
        Away_Team VARCHAR(255),
        Home_Score INT,
        Away_Score INT
    )
    """
    cursor.execute(create_table_query)

    # Insert data from the DataFrame into the MySQL table
    for i, row in data.iterrows():
        insert_query = """
        INSERT INTO laliga_matches (League, Date, Home_Team, Away_Team, Home_Score, Away_Score)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            row['League'],
            row['Date'],
            row['Home Team'],
            row['Away Team'],
            row['Home Score'],
            row['Away Score']
        ))

    # Commit the transaction
    conn.commit()

    print("Data saved successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the connection
    cursor.close()
    conn.close()
