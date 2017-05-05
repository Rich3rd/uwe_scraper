import unittest
from Scraper import login


class TestCases(unittest.TestCase):
    def test_login_pass(self):
       session = login('username', '1244234235')
       self.assertIsNotNone(session)

    def test_login_fail(self):
        session = login('username', 'password')
        self.assertIsNone(session)

if __name__ == '__main__':
    unittest.main()
