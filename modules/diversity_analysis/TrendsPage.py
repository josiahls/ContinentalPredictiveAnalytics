import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import dash
from pathlib import Path
import os
from dash.dependencies import Input, Output
from core.module import Module
from util.utility import Utility
import numpy as np

from core import Page

ut = Utility('TrendsPage')


class TrendsPage(Page):
    def __init__(self):
        """
        This is the core page. One of the main functions of it is to
        return a view that dash can handle.
        """
        super().__init__()
        read_limit = None
        # Get the current work space
        self.data_workspace = str(Path(__file__).parents[0])
        self.data_workspace += os.sep

        self.csv_locations = ['master.csv', 'code_table.csv']

        self.unique_values = {}
        self.categories = {}

    def get_view(self):
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='diversity_category',
                    options=[{'label': i, 'value': i} for i in ['hrlo', 'htrht']],
                    value='all'
                ),
                dcc.Dropdown(
                    id='diversity_unique_value_dropdown',
                    options=[{'label': i, 'value': i} for i in ['greteg', 'gttrgrtg']],
                    multi=True,
                    value='all'
                ),
            ], style={'width': '49%', 'display': 'inline-block'}),

            dcc.Graph(id='diversity_trends')
        ])

    def set_callbacks(self, app=dash.Dash()):
        @app.callback(Output('diversity_trends', 'figure'), [Input('diversity_unique_value_dropdown', 'value')])
        def update_graph(diversity_unique_value_dropdown):
            return {
                'data': [{
                    'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'y': [7, 6, 3, 2, 5, 7, 8, 6, 5, 3]
                }]
            }

        @app.callback(Output('diversity_unique_value_dropdown', 'options'), [Input('diversity_category', 'value')])
        def update_graph(diversity_category):
            return [{'label': 3, 'value': 3}]

    def get_page_id(self):
        return 'page__diversity_trends'

    def get_page_name(self):
        return 'Trends'
