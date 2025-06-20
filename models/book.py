import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from utils.db import DB_NAME

class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author

    def save(self):
        try:
            with sqlite3.connect(DB_NAME, timeout=5) as conn:
                conn.execute("INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)",
                             (self.isbn, self.title, self.author))
                print("✅ Book added successfully.")
        except sqlite3.Error as e:
            print(f"❌ Failed to save book: {e}")

    @staticmethod
    def delete(isbn):
        try:
            with sqlite3.connect(DB_NAME, timeout=5) as conn:
                conn.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
                print("✅ Book deleted successfully.")
        except sqlite3.Error as e:
            print(f"❌ Failed to delete book: {e}")