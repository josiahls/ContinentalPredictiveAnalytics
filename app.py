# -*- coding: utf-8 -*-
import importlib
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from core import Module
from util.bcolors import bcolors as b
from util.utility import Utility

LIST_OF_MODULE_INSTANCES = []


def load_modules():
    print(ut.context(os.listdir('modules').__str__()))
    module_base = 'modules'

    # Go through the modules directory
    for module_dir in os.listdir(module_base):
        # check if the directory is a .py file, then skip
        if module_dir.__contains__('.py'):
            continue
        # Possible module name
        for module_class_file in os.listdir(module_base + os.sep + module_dir):
            # The base module file should have a file
            # that is the base module name
            if module_class_file.lower().__contains__('module'):
                # is the the import statement. It should read:
                # from modules.[module_dir_name].[module_class_file] import [module_class_file]
                module_import = module_base + '.' + module_dir + '.' + module_class_file[:-3]
                module_instance = importlib.__import__(module_import, fromlist=[module_class_file[:-3]])

                # creates an instance of the class
                class_instance = getattr(module_instance, module_class_file[:-3])
                analysis_module_instance = class_instance()

                # checks if it is a child of the Module class
                ut.context(str(analysis_module_instance.__str__))
                ut.context('Is is this an instance of module: ' + str(isinstance(analysis_module_instance, Module)))
                if isinstance(analysis_module_instance, Module):
                    ut.context('Adding ' + str(analysis_module_instance.__class__) + " to tab list")
                    # loads the list of module instances
                    LIST_OF_MODULE_INSTANCES.append(analysis_module_instance)
                else:
                    ut.context(b.FAIL + 'Module is not correct instance' + b.ENDC)
            elif not module_class_file.lower().__contains__('__init__') and \
                    not module_class_file.lower().__contains__('__pycache__'):
                ut.context(b.WARNING + 'No module called ' + module_class_file + ' exists. You need to have "module" '
                                                                                 'somewhere in the name. Like '
                                                                                 '"BasicModuleTester' + b.ENDC)


# Initialize local fields
ut = Utility('app')

# Initialize modules
load_modules()

# Set the tabs array
tabs = []
for analysis_module in LIST_OF_MODULE_INSTANCES:
    tabs.append({'label': analysis_module.get_module_name(), 'value': analysis_module.get_tab_value()})
    ut.context(tabs.__str__())

# Initialize the app dash object
app = dash.Dash()

# Set the layout from the modules
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    html.Div(
        [
            dcc.Tabs(
                tabs=tabs,
                value=tabs[0].get('value'),
                id='tabs',
            ),
        ],
        style={
            'width': '100%',
            'fontFamily': 'Sans-Serif',
            'color': 'black',
            'margin-left': 'auto',
            'margin-right': 'auto',
        }
    ),
    html.Div(
        html.Div(id='tab-output'),
        style={'width': '100%', 'float': 'right'}
    )
])


@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    for analysis_module in LIST_OF_MODULE_INSTANCES:
        if analysis_module.get_tab_value() == value:
            return analysis_module.get_view()


if __name__ == '__main__':
    app.run_server(debug=True)
