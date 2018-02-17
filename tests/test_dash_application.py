import unittest
import app as a


class test_dash_application(unittest.TestCase):
    def test_load_modules(self):
        a.load_modules()
