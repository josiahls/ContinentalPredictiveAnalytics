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

        self.csv_locations = {'Linear Regression': ['parsed_gender_regression.csv',
                                                    'parsed_EmployeeSubgroup_regression.csv',
                                                    'parsed_city_regression.csv'],
                              'Arima': ['parsed_gender_2016.csv', 'parsed_employee_subgroup_2016.csv',
                                        'parsed_city_2016.csv'],
                              'Original Data': ['Original_Dataset_GenderKey.csv',
                                                'Original_Dataset_EmployeeSubgroup.csv',
                                                'Original_Dataset_City.csv',
                                        ]
                              }

        self.master = {'Arima': pd.read_csv(self.data_workspace + self.csv_locations['Arima'][0])}
        self.category_name = 'Gender Key'

        self.plots = {}
        self.plots['Arima'] = {}
        for unique_value in self.master['Arima']['Gender Key'].unique():
            self.plots['Arima'][unique_value] = self.master['Arima'][self.master['Arima']['Gender Key'] == unique_value]
            self.plots['Arima'][unique_value] = self.plots['Arima'][unique_value].groupby('Entry')

        self.diversity_models = ['Original Data', 'Arima', 'Linear Regression']
        self.unique_values = {}
        self.categories = {}

    def get_view(self):
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='diversity_model_old',
                    options=[{'label': i, 'value': i} for i in ['Original Data', 'Arima', 'Linear Regression']],
                    multi=True,
                    value='Arima'
                ),
                dcc.Dropdown(
                    id='diversity_category_old',
                    options=[{'label': i, 'value': i} for i in ['Gender Key', 'Employee Subgroup', 'City']],
                    value='Gender Key'
                ),
                dcc.Dropdown(
                    id='diversity_unique_value_dropdown_old',
                    options=[{'label': i, 'value': i} for i in [self.master['Arima'][self.category_name].unique()]],
                    multi=True,
                    value=self.master['Arima'][self.category_name].unique()[0]
                ),
            ], style={'width': '49%', 'display': 'inline-block'}),

            dcc.Graph(id='diversity_trends_old')
        ])

    def set_callbacks(self, app=dash.Dash()):
        @app.callback(Output('diversity_unique_value_dropdown_old', 'options'), [Input('diversity_category_old', 'value'),
                                                                             Input('diversity_model_old', 'value')])
        def update_graph_dropdown(diversity_category_old, diversity_model_old):
            if type(diversity_model_old) is str:
                diversity_model_old = [diversity_model_old]
            self.diversity_models = diversity_model_old

            for model in diversity_model_old:
                if diversity_category_old == 'Gender Key':
                    self.plots[model] = {}
                    self.master[model] = pd.read_csv(self.data_workspace + self.csv_locations[model][0])
                    self.category_name = 'Gender Key'
                    ut.context("Plots are: " + str(self.plots) + diversity_category_old)

                    for unique_value in self.master[model][self.category_name].unique():
                        self.plots[model][unique_value] = self.master[model][
                            self.master[model][self.category_name] == unique_value]
                        self.plots[model][unique_value] = self.plots[model][unique_value].groupby('Entry')

                    ut.context("Plots are: " + str(self.plots) + diversity_category_old)
                elif diversity_category_old == 'Employee Subgroup':
                    self.plots[model] = {}
                    self.master[model] = pd.read_csv(self.data_workspace + self.csv_locations[model][1])
                    self.category_name = 'Employee Subgroup'
                    ut.context("Plots are: " + str(self.plots) + diversity_category_old)

                    for unique_value in self.master[model][self.category_name].unique():
                        self.plots[model][unique_value] = self.master[model][
                            self.master[model][self.category_name] == unique_value]
                        self.plots[model][unique_value] = self.plots[model][unique_value].groupby('Entry')

                    ut.context("Plots are: " + str(self.plots) + diversity_category_old)

                else:
                    self.plots[model] = {}
                    self.master[model] = pd.read_csv(self.data_workspace + self.csv_locations[model][2])
                    self.category_name = 'Personnel city'
                    ut.context("Plots are: " + str(self.plots) + diversity_category_old)

                    for unique_value in self.master[model][self.category_name].unique():
                        self.plots[model][unique_value] = self.master[model][
                            self.master[model][self.category_name] == unique_value]
                        self.plots[model][unique_value] = self.plots[model][unique_value].groupby('Entry')

                    ut.context("Plots are: " + str(self.plots) + diversity_category_old)

            return [{'label': value, 'value': value} for value in
                    self.master[diversity_model_old[0]][self.category_name].unique()]

        @app.callback(Output('diversity_trends_old', 'figure'), [Input('diversity_unique_value_dropdown_old', 'value'),
                                                             Input('diversity_model_old', 'value')])
        def update_graph(diversity_unique_value_dropdown_old, diversity_model_old):
            data = []
            x = []
            y = []
            has_forecast = False

            ut.context("Made it here")

            current_year = datetime.datetime.now().date().year - 2

            if type(diversity_unique_value_dropdown_old) is str:
                diversity_unique_value_dropdown_old = [diversity_unique_value_dropdown_old]
            if type(diversity_model_old) is str:
                diversity_model_old = [diversity_model_old]

            colors = plotly.colors.DEFAULT_PLOTLY_COLORS
            index = 0
            for model in diversity_model_old:
                for unique_value in diversity_unique_value_dropdown_old:
                    x = []
                    y = []
                    ut.context(str(unique_value) + " model: " + str(diversity_model_old) + " " + str(self.plots))

                    for group in self.plots[model][unique_value].groups:
                        x.append(group)
                        y.append(len(self.plots[model][unique_value].get_group(group).index))
                        if current_year <= int(group):
                            has_forecast = True
                            break

                    name = unique_value
                    if not has_forecast:
                        name += ': Missing forecast'

                    data.append(Scatter(
                        x=x,
                        y=y,
                        name=str(model) + name,
                        mode='lines',
                        connectgaps=True,
                        line=dict(
                            color=colors[index],
                            width=2, )
                    ))
                    # Add prediction
                    x = []
                    y = []
                    for group in self.plots[model][unique_value].groups:
                        if current_year <= int(group):
                            x.append(group)
                            y.append(len(self.plots[model][unique_value].get_group(group).index))

                    data.append(Scatter(
                        x=x,
                        y=y,
                        name=str(model) + ' ' + unique_value + ' forecast',
                        mode='lines+markers',
                        connectgaps=True,
                        line=dict(
                            color=colors[index],
                            width=2, )
                    ))

                    index = index + 1 if index < len(colors) else 0

            return {
                'data': data
            }

    def get_page_id(self):
        return 'page__diversity_trends_old'

    def get_page_name(self):
        return 'Trends'
