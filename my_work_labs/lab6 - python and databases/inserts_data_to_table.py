# inserts data into the books table
# Authored: Stephen Kerr

# imports
import mysql.connector
from config import db_connection as cfg

# create a connection to the database
connection = mysql.connector.connect(
    host=cfg['host'],
    user=cfg['user'],
    password=cfg['password'],
    database='wsaa'
)

# cursor to execute SQL commands
cursor = connection.cursor()

# insert data into the books table
cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", ("harry potter", "JK Rowling"))

# print success message
print("Data inserted successfully!")

# commit the transaction
connection.commit()

# close the cursor
cursor.close()

# close the connection
connection.close()
