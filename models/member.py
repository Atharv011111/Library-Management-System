import sqlite3
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from utils.db import DB_NAME
from utils.date_utils import calculate_late_fee

class Member:
    def __init__(self, member_id, name, role='member'):
        self.member_id = member_id
        self.name = name
        self.role = role

    def register(self):
        try:
            with sqlite3.connect(DB_NAME, timeout=5) as conn:
                conn.execute("INSERT INTO members (id, name, role) VALUES (?, ?, ?)", (self.member_id, self.name, self.role))
                print("✅ Member registered successfully.")
        except sqlite3.Error as e:
            print(f"❌ Failed to register member: {e}")

    def borrow_book(self, isbn):
        try:
            with sqlite3.connect(DB_NAME, timeout=5) as conn:
                conn.execute("UPDATE books SET available = 0 WHERE isbn = ?", (isbn,))
                conn.execute("INSERT INTO borrow_history (member_id, isbn, borrow_date) VALUES (?, ?, ?)",
                             (self.member_id, isbn, datetime.today().strftime('%Y-%m-%d')))
                print("✅ Book borrowed successfully.")
        except sqlite3.Error as e:
            print(f"❌ Failed to borrow book: {e}")

    def return_book(self, isbn):
        try:
            return_date = datetime.today().strftime('%Y-%m-%d')
            with sqlite3.connect(DB_NAME, timeout=5) as conn:
                row = conn.execute("SELECT borrow_date FROM borrow_history WHERE member_id = ? AND isbn = ? AND return_date IS NULL",
                                   (self.member_id, isbn)).fetchone()
                if not row:
                    print("❌ No borrow record found for return.")
                    return
                borrow_date = row[0]
                late_fee = calculate_late_fee(borrow_date, return_date)
                conn.execute("UPDATE books SET available = 1 WHERE isbn = ?", (isbn,))
                conn.execute("""
                    UPDATE borrow_history SET return_date = ?, late_fee = ?
                    WHERE member_id = ? AND isbn = ? AND return_date IS NULL
                """, (return_date, late_fee, self.member_id, isbn))
                print(f"✅ Book returned successfully. Late fee: ₹{late_fee}")
        except sqlite3.Error as e:
            print(f"❌ Failed to return book: {e}")

    def view_history(self):
        try:
            with sqlite3.connect(DB_NAME, timeout=5) as conn:
                rows = conn.execute("SELECT isbn, borrow_date, return_date, late_fee FROM borrow_history WHERE member_id = ?",
                                    (self.member_id,)).fetchall()
                for row in rows:
                    print(f"ISBN: {row[0]}, Borrowed: {row[1]}, Returned: {row[2] if row[2] else 'Not yet returned'}, Late Fee: ₹{row[3]}")
        except sqlite3.Error as e:
            print(f"❌ Failed to fetch history: {e}")