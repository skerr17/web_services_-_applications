# this program will view data in a table
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

# execute a query to delete a book with a specific ID from the books table
cursor.execute("DELETE FROM books WHERE ID = %s", (1,))

# print success message
print("Data deleted successfully!")

# commit the transaction
connection.commit()

# close the cursor
cursor.close()
# close the connection
connection.close()
