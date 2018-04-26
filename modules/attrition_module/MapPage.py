import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import dash
from pathlib import Path
import os
from dash.dependencies import Input, Output
from core.module import Module
from modules.attrition_module.DateSliderView import DateSlider
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

        ut.context(str(self.master_csv))
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
        self.range_slider = DateSlider()

        self.views = []
        self.views.append(self.unitedStatesMapView)

    def get_view(self):
        self.unitedStatesMapView.setFields(category=self.categories[2], unique_values=self.unique_values,
                                           date_slider=set(self.date_range))
        self.range_slider.set_fields(self.date_range)

        return html.Div([
            html.Div([
                html.Div([
                    html.H3('Categories', style={'color': 'rgb(254, 165, 1)'}),
                    dcc.Dropdown(
                        id='category_dropdown',
                        options=[{'label': i, 'value': i} for i in self.categories],
                        value=self.categories[2]
                    ),
                ],
                    style={'width': '49%', 'display': 'inline-block', 'padding': '0px'}),

                html.Div([

                    html.H3('Values', style={'color': 'rgb(254, 165, 1)'}),
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
            self.range_slider.get_view(),
            dcc.Graph(id='attrition_map_graph', figure=self.unitedStatesMapView.get_view()),

        ], style={'width': '100%','color':'black', 'display': 'inline-block', })

    def set_callbacks(self, app=dash.Dash()):
        for view in self.views:
            view.set_callbacks(app)

        @app.callback(Output('unique_value_dropdown', 'options'), [Input('category_dropdown','value')])
        def set_unqiue_values(category_dropdown):
            return [{'label': i, 'value': i} for i in self.unique_values[category_dropdown]]

    def get_page_id(self):
        return 'page_map'

    def get_page_name(self):
        return 'Map'
