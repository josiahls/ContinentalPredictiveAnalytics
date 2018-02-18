from core.module import Module
import dash_core_components as dcc


class BasicTestModule(Module):
    def __init__(self):
        super().__init__()

    def get_view(self):
        return dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [10, 20, 30], 'y': [4, 1, 2], 'type': 'bar', 'name': 'hebron'},
                    {'x': [1, 2, 3], 'y': [20, 40, 50], 'type': 'bar', 'name': u'billy road'},
                ],
                'layout': {

                    'title': 'Josiah\'s Dash Data Visualization'

                }
            }
        )

    def get_module_name(self):
        return "Basic Tester2!!"

    def get_tab_value(self):
        return "tab_basic2"

    def __str__(self):
        return "hello"
