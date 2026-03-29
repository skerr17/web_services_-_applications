# this module contains the code to 
# interact with the books database
# CRUD operations
# Authored: Stephen Kerr

# imports
import mysql.connector
from config import db_connection as cfg

class BooksDAO:
    def __init__(self):
        # create a connection to the database
        self.connection = mysql.connector.connect(
            host=cfg['host'],
            user=cfg['user'],
            password=cfg['password'],
            database='wsaa'
        )
        # cursor to execute SQL commands
        self.cursor = self.connection.cursor()

    def create_book(self, title, author):
        # insert data into the books table
        self.cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        # commit the transaction
        self.connection.commit()
        print("Data inserted successfully!")
        return self.cursor.lastrowid

    def read_books(self):
        # execute a query to select all data from the books table
        self.cursor.execute("SELECT * FROM books")
        # fetch all results
        results = self.cursor.fetchall()
        return results

    def update_book(self, book_id, title, author):
        # execute a query to update a book with a specific ID in the books table
        self.cursor.execute("UPDATE books SET title = %s, author = %s WHERE id = %s", (title, author, book_id))
        # commit the transaction
        self.connection.commit()
        print("Data updated successfully!")

    def delete_book(self, book_id):
        # execute a query to delete a book with a specific ID from the books table
        self.cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        # commit the transaction
        self.connection.commit()
        print("Data deleted successfully!")

    def close_connection(self):
        # close the cursor and connection
        self.cursor.close()
        self.connection.close()

    def find_book_by_id(self, book_id):
        # execute a query to find a book by ID
        self.cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        result = self.cursor.fetchone()
        return result
    
booksDAO = BooksDAO()