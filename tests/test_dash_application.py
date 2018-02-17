import unittest


class test_dash_application(unittest.TestCase):
    def test_load_modules(self):
        import app as a
        a.load_modules()
