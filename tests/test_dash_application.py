import unittest


class test_dash_application(unittest.TestCase):
    def test_load_modules(self):
        import dash_html_components as html
        import app as a
        a.load_modules()
