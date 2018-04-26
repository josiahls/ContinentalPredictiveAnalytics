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
import plotly
from plotly.graph_objs import *

ut = Utility('TrendsPageNew')


class TrendsPageNew(Page):
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

        self.csv_locations = {'Linear Regression': ['parsed_gender_regression.csv',
                                                    'parsed_EmployeeSubgroup_regression.csv',
                                                    'parsed_city_regression.csv'],
                              'Arima': ['parsed_gender_2016.csv', 'parsed_employee_subgroup_2016.csv',
                                        'parsed_city_2016.csv'],
                              'Original Data': ['Original_Dataset_GenderKey.csv',
                                                'Original_Dataset_EmployeeSubgroup.csv',
                                                'Original_Dataset_City.csv']
                              }

    def get_view(self):
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='diversity_model',
                    options=[{'label': i, 'value': i} for i in ['Original Data', 'Arima', 'Linear Regression']],
                    multi=True,
                    value='Arima'
                ),
                dcc.Dropdown(
                    id='diversity_category',
                    options=[{'label': i, 'value': i} for i in ['Gender Key', 'Employee Subgroup', 'City']],
                    value='Gender Key'
                ),
                dcc.Dropdown(
                    id='diversity_unique_value_dropdown',
                    options=[{'label': i, 'value': i} for i in ['hi']],
                    multi=True,
                    value='hi'
                ),
            ], style={'width': '49%', 'display': 'inline-block'}),

            dcc.Graph(id='diversity_trends')
        ])

    def set_callbacks(self, app=dash.Dash()):
        pass

    def get_page_id(self):
        return 'page__diversity_trends_new'

    def get_page_name(self):
        return 'Trends'
