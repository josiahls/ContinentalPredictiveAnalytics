import unittest


class test_ObjectForTesting(unittest.TestCase):
    def test_object_test_adder(self):
        print("Startinging")
        from ObjectForTesting import ObjectForTesting
        m = ObjectForTesting()
        k = m.adder(1, 1)
        self.assertEqual(k, 2, 'The numbers are not adding properly')
        k = m.adder(1, 2)
        self.assertEqual(k, 3, 'The numbers are not adding properly')
        k = m.adder(2, 2)
        self.assertEqual(k, 4, 'The numbers are not adding properly')
