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
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {

                    'title': 'Josiah\'s Dash Data Visualization'

                }
            }
        )

    def get_module_name(self):
        return "Basic Tester!!"

    def get_tab_value(self):
        return "tab_basic"

    def __str__(self):
        return "hello"
