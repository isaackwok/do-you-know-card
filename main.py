import unittest
from main import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        pass

    def test_num1(self):
        rv = self.app.get('/')
        assert b'Hello world' in rv.data


if __name__ == '__main__':
    unittest.main()