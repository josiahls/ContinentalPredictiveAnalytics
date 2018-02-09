import unittest

class ObjectTest(unittest.TestCase):
    def test_object_test_adder(self):
        from ObjectForTesting import ObjectForTesting
        m = ObjectForTesting()
        k = m.adder(1,1)
        self.assertEquals(k, 1, 'The numbers are not multiplying properly')
        k = m.adder(1, 2)
        self.assertEquals(k, 3, 'The numbers are not multiplying properly')
        k = m.adder(2, 2)
        self.assertEquals(k, 4, 'The numbers are not multiplying properly')
