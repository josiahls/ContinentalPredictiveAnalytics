import unittest


class ObjectTest(unittest.TestCase):
    def test_object_test_adder(self):
        print("Startinging")
        from ObjectForTesting import ObjectForTesting
        m = ObjectForTesting()
        k = m.adder(1, 1)
        self.assertEqual(k, 1, 'The numbers are not multiplying properly')
        k = m.adder(1, 2)
        self.assertEqual(k, 3, 'The numbers are not multiplying properly')
        k = m.adder(2, 2)
        self.assertEqual(k, 4, 'The numbers are not multiplying properly')
