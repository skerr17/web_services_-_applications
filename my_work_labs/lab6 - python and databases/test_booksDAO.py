# this code tests the BooksDAO class
# Authored: Stephen Kerr

# imports
from booksDAO import BooksDAO


# create an instance of the BooksDAO class
books_dao = BooksDAO()
latest_id = books_dao.create_book("harry potter", "JK Rowling")
print("Books in the database:")


# find by id
book = books_dao.find_book_by_id(latest_id)
print(book)

# update 
books_dao.update_book(latest_id, "harry potter and the chamber of secrets", "JK Rowling")
book = books_dao.find_book_by_id(latest_id)
print(book)

# get all books
books = books_dao.read_books()
for book in books:
    print(book)

# delete the book
books_dao.delete_book(latest_id)
# get all books after deletion
books = books_dao.read_books()
for book in books:
    print(book)

# close the connection
books_dao.close_connection()
print("Connection closed.")
