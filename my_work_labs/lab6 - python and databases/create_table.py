# creates a SQL table
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

# create table
cursor.execute("""CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255)
)""")

# close the cursor
cursor.close()

# close the connection
connection.close()

