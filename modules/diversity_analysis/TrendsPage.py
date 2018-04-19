import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd
from dash import dash
from pathlib import Path
import os
from dash.dependencies import Input, Output
from core.module import Module
from util.utility import Utility
import numpy as np

from core import Page
import plotly.plotly as py
from plotly.graph_objs import *

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

        self.csv_locations = ['parsed_gender_csv.csv']

        self.master = pd.read_csv(self.data_workspace + self.csv_locations[0])
        self.category_name = 'Gender Key'

        self.plots = {}
        for unique_value in self.master['Gender Key'].unique():
            self.plots[unique_value] = self.master[self.master['Gender Key'] == unique_value]
            self.plots[unique_value] = self.plots[unique_value].groupby('Entry')

        self.unique_values = {}
        self.categories = {}

    def get_view(self):
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='diversity_category',
                    options=[{'label': i, 'value': i} for i in [self.category_name]],
                    value=self.category_name
                ),
                dcc.Dropdown(
                    id='diversity_unique_value_dropdown',
                    options=[{'label': i, 'value': i} for i in [self.master[self.category_name].unique()]],
                    multi=True,
                    value=self.master[self.category_name].unique()[0]
                ),
            ], style={'width': '49%', 'display': 'inline-block'}),

            dcc.Graph(id='diversity_trends')
        ])

    def set_callbacks(self, app=dash.Dash()):
        @app.callback(Output('diversity_trends', 'figure'), [Input('diversity_unique_value_dropdown', 'value')])
        def update_graph(diversity_unique_value_dropdown):
            data = []
            x = []
            y = []

            current_year = datetime.datetime.now().date().year

            if type(diversity_unique_value_dropdown) is str:
                diversity_unique_value_dropdown = [diversity_unique_value_dropdown]

            for unique_value in diversity_unique_value_dropdown:
                x = []
                y = []
                for group in self.plots[unique_value].groups:
                    x.append(group)
                    y.append(self.plots[unique_value].get_group(group).size)
                    if current_year <= int(group):
                        break

                data.append(Scatter(
                    x=x,
                    y=y,
                    name=unique_value
                ))
                # Add prediction
                x = []
                y = []
                for group in self.plots[unique_value].groups:
                    if current_year <= int(group):
                        x.append(group)
                        y.append(self.plots[unique_value].get_group(group).size)

                data.append(Scatter(
                    x=x,
                    y=y,
                    name=unique_value + ' forecast',
                    fillcolor='rgb(255, 153, 0, 0.2)',
                ))

            return {
                'data': data
            }

        @app.callback(Output('diversity_unique_value_dropdown', 'options'), [Input('diversity_category', 'value')])
        def update_graph(diversity_category):
            return [{'label': value, 'value': value} for value in self.master[diversity_category].unique()]

    def get_page_id(self):
        return 'page__diversity_trends'

    def get_page_name(self):
        return 'Trends'
