import sys
import os
import sqlite3

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
from models.book import Book
from models.member import Member
from utils.db import init_db, DB_NAME

init_db()

def admin_menu():
    while True:
        print("""
        Admin Menu:
        1. Register Member
        2. Register Admin
        3. Add Book
        4. Delete Book
        5. Logout
        """)
        choice = input("Enter choice: ")
        if choice == '1':
            mid = input("Member ID: ")
            name = input("Name: ")
            Member(mid, name).register()
        elif choice == '2':
            aid = input("Admin ID: ")
            name = input("Name: ")
            Member(aid, name, role='admin').register()
        elif choice == '3':
            isbn = input("ISBN: ")
            title = input("Title: ")
            author = input("Author: ")
            Book(isbn, title, author).save()
        elif choice == '4':
            isbn = input("ISBN to delete: ")
            Book.delete(isbn)
        elif choice == '5':
            break

def member_menu(member_id):
    while True:
        print("""
        Member Menu:
        1. Borrow Book
        2. Return Book
        3. View Borrow History
        4. Logout
        """)
        choice = input("Enter choice: ")
        member = Member(member_id, "")
        if choice == '1':
            isbn = input("Book ISBN: ")
            member.borrow_book(isbn)
        elif choice == '2':
            isbn = input("Book ISBN: ")
            member.return_book(isbn)
        elif choice == '3':
            member.view_history()
        elif choice == '4':
            break

def main():
    while True:
        print("""
        Welcome to Library System
        1. Login as Admin
        2. Login as Member
        3. Exit
        """)
        role = input("Choose role: ")
        if role == '1':
            admin_id = input("Enter Admin ID: ")
            try:
                with sqlite3.connect(DB_NAME, timeout=5) as conn:
                    user = conn.execute("SELECT role, name FROM members WHERE id = ?", (admin_id,)).fetchone()
                    if user and user[0] == 'admin':
                        print(f"✅ Welcome Admin: {user[1]}")
                        admin_menu()
                    else:
                        print("❌ Access denied. Not an admin.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif role == '2':
            member_id = input("Enter Member ID: ")
            try:
                with sqlite3.connect(DB_NAME, timeout=5) as conn:
                    user = conn.execute("SELECT role, name FROM members WHERE id = ?", (member_id,)).fetchone()
                    if user and user[0] == 'member':
                        print(f"✅ Welcome Member: {user[1]}")
                        member_menu(member_id)
                    else:
                        print("❌ Access denied. Not a member.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif role == '3':
            break

if __name__ == '__main__':
    main()