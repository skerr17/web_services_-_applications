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

# execute a query to select all data from the books table
cursor.execute("SELECT * FROM books")

# fetch all results
results = cursor.fetchall()
# print the results
for row in results:
    print(row)

# close the cursor
cursor.close()
# close the connection
connection.close()
