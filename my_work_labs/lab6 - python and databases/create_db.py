# create a databases 
# Authored: Stephen Kerr

import mysql.connector

from config import db_connection as cfg

# create a connection to the database
connection = mysql.connector.connect(
    host=cfg['host'],
    user=cfg['user'],
    password=cfg['password']
)

# cursor to execute SQL commands
cursor = connection.cursor()

# create database
cursor.execute("CREATE DATABASE wsaa")

# close the cursor
cursor.close()

# close the connection
connection.close()
