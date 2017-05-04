import unittest
from Scraper import login


class TestCases(unittest.TestCase):
    def test_login(self):
       session = login('n2-terjing', 'vellapushFare19')
       self.assertIsNotNone(session, 'ITS NOT NULL')


if __name__ == '__main__':
    unittest.main()
