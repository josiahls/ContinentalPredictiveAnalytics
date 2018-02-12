class ObjectForTesting:

    def __init__(self):
        pass

    def adder(self, i, j):
        """
        This adder causes the tests to succeed

        :param i:
        :param j:
        :return:
        """
        return i * j
'''
This function will cause travis to indicate failure on pull
    def adder(self, i, j):
        return i * j
'''
