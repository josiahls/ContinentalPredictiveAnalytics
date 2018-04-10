import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import dash
from pathlib import Path
import os
from dash.dependencies import Input, Output
from core.module import Module
from modules.attrition_module.UnitedStatesMapView import UnitedStatesMapView
from util.utility import Utility
import numpy as np

from core import Page

ut = Utility('MapPage')

class MapPage(Page):
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

        self.master_csv = {}
        # Add the locations to the master pd
        for location in self.csv_locations:
            if location.__contains__('.xlsx'):
                data = pd.read_excel(self.data_workspace + location).iloc[:read_limit]
                self.master_csv[location.split('.xlsx')[0]] = data
            if location.__contains__('.csv'):
                data = pd.read_csv(self.data_workspace + location, nrows=read_limit)
                self.master_csv[location.split('.csv')[0]] = data

        # ut.context(str(self.master_csv))
        ut.context('Merging')

        # Merge All CSVs into one set
        self.master_csv['local'] = pd.DataFrame()
        for i, label in enumerate(self.master_csv):
            # ut.context("minimum is: " + str(minimum))
            if i != 0 and label != 'local':
                self.master_csv['local'] = pd.DataFrame(self.master_csv['local']).merge(
                    pd.DataFrame(self.master_csv[label]), suffixes=['_1', '_2'], on='Location.Code',
                    sort=True, how='left', copy=True)
            elif i == 0:
                self.master_csv['local'] = pd.DataFrame(self.master_csv[label])

        # ut.context(str(self.master_csv))
        pd.DataFrame(self.master_csv['local']).to_csv(self.data_workspace + 'josiah_local.csv')
        self.current_category = 'Gender'
        self.unique_values = {}

        self.current_category = 'Gender'
        self.categories = [label for label in self.master_csv['local']]
        self.date_range = [date for date in pd.DatetimeIndex(self.master_csv['local']['Hire.Date']).year]

        for label in self.categories:
            not_nan_values = pd.DataFrame(self.master_csv['local'][label]).dropna()
            self.unique_values[label] = not_nan_values[label].unique()
            self.unique_values[label] = np.append(self.unique_values[label], 'all')

        # Set views
        self.unitedStatesMapView = UnitedStatesMapView(data=self.master_csv['local'])

        self.views = []
        self.views.append(self.unitedStatesMapView)

    def get_view(self):
        self.unitedStatesMapView.setFields(category=self.categories[2], unique_values=self.unique_values)

        return html.Div([
            html.Div([
                html.Div([
                    html.H3('Categories'),
                    dcc.Dropdown(
                        id='category_dropdown',
                        options=[{'label': i, 'value': i} for i in self.categories],
                        value=self.categories[2]
                    ),
                ],
                    style={'width': '49%', 'display': 'inline-block', 'padding': '0px'}),

                html.Div([

                    html.H3('Values'),
                    dcc.Dropdown(
                        id='unique_value_dropdown',
                        options=[{'label': i, 'value': i} for i in self.unique_values[self.categories[2]]],
                        multi=True,
                        value='all'
                    ),
                ],
                    style={'width': '49%', 'display': 'inline-block', }),
            ], style={'width': '100%', 'display': 'inline-block', },

            ),

            html.H3('Unit Options'),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Numeric', 'Ratio']],
                value='Numeric',
            ),
            dcc.Graph(id='diversity_map_graph', figure=self.unitedStatesMapView.get_view()),
            html.Div([
                html.H3('Year'),
                dcc.RangeSlider(
                    id='my-range-slider',
                    min=min(self.date_range),
                    max=max(self.date_range),
                    value=[min(self.date_range), max(self.date_range)],
                    step=None,
                    marks={
                        str(year): {'label': str(year),
                                    'style': {'color': 'white', 'background-color': 'rgb(135,206,250)'}}
                        for year in set(self.date_range)}, ),

            ], style={'margin-left': '10px', 'width': '95%', 'align': 'center'}),
        ])

    def set_callbacks(self, app=dash.Dash()):
        self.unitedStatesMapView.set_callbacks(app)
        @app.callback(Output('category_dropdown', 'figure'), [Input('category_dropdown', 'value'),
                                                              Input('unique_value_dropdown', 'value')])
        def update_chart(category_dropdown, unique_value_dropdown):
            self.unitedStatesMapView.setFields(category=category_dropdown, unique_values=unique_value_dropdown)
            return self.unitedStatesMapView.get_view()

    def get_page_id(self):
        return 'page_map'

    def get_page_name(self):
        return 'Map'