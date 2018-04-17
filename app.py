# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import importlib
import os

from util.bcolors import bcolors as b
from util.utility import Utility

LIST_OF_MODULE_INSTANCES = []
LIST_OF_EXCLUDED_MODULES = ['__pycache__']


def load_modules():
    print(ut.context(os.listdir('modules').__str__()))
    module_base = 'modules'

    # Go through the modules directory
    for module_dir in os.listdir(module_base):
        # check if the directory is a .py file, then skip
        if module_dir.__contains__('.py'):
            continue
        # Possible module name
        found = False
        for module_class_file in os.listdir(module_base + os.sep + module_dir):
            found = False
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
                # ut.context(str(analysis_module_instance.__str__))
                # ut.context('Is is this an instance of module: ' + str(isinstance(analysis_module_instance, Module)))
                import core.module
                if isinstance(analysis_module_instance, core.Module):
                    ut.context('Adding ' + str(analysis_module_instance.__class__) + " to tab list")
                    found = True
                    # loads the list of module instances
                    LIST_OF_MODULE_INSTANCES.append(analysis_module_instance)
                    break
        if not found and module_dir not in LIST_OF_EXCLUDED_MODULES:
            ut.context(b.FAIL + 'Module is not correct instance' + b.ENDC)
            ut.context(b.WARNING + 'No module in ' + module_dir + ' exists. You need to have module" '
                                                                  'somewhere in the name. Like "BasicModuleTester. It also needs to be a child of Module' + b.ENDC)


# Initialize local fields
ut = Utility('app')
app = dash.Dash()

if __name__ == '__main__':
    # Initialize the app dash object
    app = dash.Dash()

    # Suppress those stupid callback exceptions
    app.config.supress_callback_exceptions = True

    # Initialize modules
    load_modules()

    # Set the tabs array
    tabs = []
    for analysis_module in LIST_OF_MODULE_INSTANCES:
        tabs.append({'label': analysis_module.get_module_name(), 'value': analysis_module.get_tab_value()})
        ut.context(tabs.__str__())

    # Set the layout from the modules

   ######
    app_colors = {
        'background': '#0C0F0A',
        'text': '#FFFFFF',
        'sentiment-plot': '#41EAD4',
        'volume-bar': '#FBFC74',
        'someothercolor': '#FF206E',
    }

    app.layout = html.Div([
        html.Div(
            [
                html.Img(
                    src="http://www.continentaltire.com/sites/all/themes/continental/assets/images/print-logo.jpg",
                    className='one columns',
                    style={
                        'height': '100',
                        'width': '250',
                        'float': 'left',
                        'position': 'relative',
                    },
                ),
                html.H1(
                    'HR Predictive Analysis',
                    # className='eight columns',
                    className ='p-3 mb-2 bg-secondary text-white',
                    style={'text-align': 'center', 'padding':'15px','height':'100'
                           },
                ),
            ],
            style={'height': '100','width': '100%',},
        ),



        html.Div(
            [
                dcc.Tabs(
                    tabs=tabs,
                    value=tabs[1].get('value'),
                    id='tabs',

                ),
            ],
            style={
                'width': '100%',
                'fontFamily': 'Sans-Serif',
                'color': 'black',
                'background-color' :'red',
                'margin-left': 'auto',
                'margin-right': 'auto',
            },

        ),

        html.Div(
            html.Div(id='tab-output'),
            style={'width': '100%', 'float': 'right'}
        )

        ],

    )


    @app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
    def display_content(tabs):
        ut.context("Callback executing")
        for analysis_module in LIST_OF_MODULE_INSTANCES:
            if analysis_module.get_tab_value() == tabs:
                return analysis_module.get_view()

    # Add other callbacks
    for analysis_module in LIST_OF_MODULE_INSTANCES:
            analysis_module.set_callback_function(app=app)

    # Loading screen CSS
    # app.css.append_css({"external_url": "https://josiahls.github.io/loading_screen.css"})
    app.css.append_css({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"})
    #app.css.append_css({"external_url": "https://josiahls.github.io/loading_screen.css"})
    app.server.run(debug=True, threaded=True)



