import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import dash
from pathlib import Path
import os
from dash.dependencies import Input, Output
from core.module import Module
from modules.diversity_analysis.MapPage import MapPage
from modules.diversity_analysis.TrendsPage import TrendsPage
from util.utility import Utility
import numpy as np

ut = Utility('DiversityModule')


class DiversityModule(Module):
    def __init__(self):
        super().__init__()
        # Set Pages
        self.pages = []

        self.pages.append(TrendsPage())

    def get_view(self):

        # Set the tabs array
        tabs = []
        for page in self.pages:
            tabs.append({'label': page.get_page_name(), 'value': page.get_page_id()})
            ut.context(tabs.__str__())

        return html.Div([
            html.Div(
                [
                    dcc.Tabs(
                        tabs=tabs,
                        value=tabs[0].get('value'),
                        id='module_diversity_tabs',

                    ),
                ],
                style={
                    'width': '100%',
                    'fontFamily': 'Sans-Serif',
                    'color': 'black',
                    'background-color': 'red',
                    'margin-left': 'auto',
                    'margin-right': 'auto',
                },

            ),
            html.Div(
                html.Div(id='tab_module_diversity_output'),
                style={'width': '100%', 'float': 'right'}
            )
        ])

    def get_module_name(self):
        return "Time to Hire"

    def get_tab_value(self):
        return "tab_diversity"

    def __str__(self):
        return "hello"

    def set_callback_function(self, app=dash.Dash()):
        for page in self.pages:
            page.set_callbacks(app=app)

        @app.callback(Output('tab_module_diversity_output', 'children'), [Input('module_diversity_tabs', 'value')])
        def display_content(module_diversity_tabs):
            ut.context("Callback is executing")
            for page in self.pages:
                if page.get_page_id() == module_diversity_tabs:
                    return page.get_view()
