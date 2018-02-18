import inspect

CLASS_TO_SHOW = 'all'


class Utility:
    def __init__(self, tag='Utility:'):
        self.tag = tag

    def context(self, msg='', print_in_method=True):
        display = self.tag + ':' + str(inspect.stack()[1][3]) + ': ' + msg
        if print_in_method and (CLASS_TO_SHOW == 'all' or display.lower().__contains__(CLASS_TO_SHOW)):
            print(display)
        elif not print_in_method and (CLASS_TO_SHOW == 'all' or display.lower().__contains__(CLASS_TO_SHOW)):
            return display
        else:
            return ''
