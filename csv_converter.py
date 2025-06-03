import sqlite3
import csv

# Connect to your SQLite database
conn = sqlite3.connect('login.db')  # Replace with your database filename
cursor = conn.cursor()

# Query the database (adjust the table name as needed)
cursor.execute("SELECT * FROM users")  # Replace 'users' with your table name

# Fetch all the rows from the query result
rows = cursor.fetchall()

# Get the column names (optional, if you want them as headers in the CSV)
columns = [description[0] for description in cursor.description]

# Create or open the CSV file to write the data
with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the column headers (optional)
    writer.writerow(columns)
    
    # Write all the rows
    writer.writerows(rows)

# Close the database connection
conn.close()

print("Database contents have been written to 'output.csv'.")
