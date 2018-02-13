import inspect

class Utility():
    def __init__(self, tag='Utility:'):
        self.tag = tag

    def context(self):
        return self.tag + ':' + str(inspect.stack()[1][3]) + ': '
