import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

from models.member import Member
from models.book import Book
from utils.date_utils import calculate_late_fee

class TestLibrarySystem(unittest.TestCase):
    def test_late_fee(self):
        self.assertEqual(calculate_late_fee('2025-06-01', '2025-06-10'), 2)
        self.assertEqual(calculate_late_fee('2025-06-01', '2025-06-07'), 0)

    def test_book_and_member_registration(self):
        member = Member("T001", "Test User")
        member.register()
        book = Book("987654", "Test Book", "Test Author")
        book.save()

    def test_borrow_return(self):
        member = Member("T002", "User2")
        member.register()
        book = Book("654321", "Another Book", "Author")
        book.save()
        member.borrow_book("654321")
        member.return_book("654321")

if __name__ == '__main__':
    unittest.main()
