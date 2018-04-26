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

        self.csv_locations = {'Regression Analysis': ['parsed_gender_regression.csv',
                                                      'parsed_EmployeeSubgroup_regression.csv',
                                                      'parsed_city_regression.csv'],
                              'Arima': ['parsed_gender_ARIMA.csv', 'parsed_employee_subgroup_ARIMA.csv',
                                        'parsed_city_ARIMA.csv'],
                              'Original Data': ['Original_Dataset_GenderKey.csv',
                                                'Original_Dataset_EmployeeSubgroup.csv',
                                                'Original_Dataset_City.csv']
                              }
        # Load the master dictionary of all the csvs
        self.master = {}
        for model in self.csv_locations:
            self.master[model] = {}
            for csv in self.csv_locations[model]:
                ut.context("Loading csv at key: " + str(model) + " " + str(csv))
                self.master[model][csv] = pd.read_csv(self.data_workspace + csv)
        # ut.context(str(self.master))

        # Load all the plots for the graph
        pre_plots = {}
        for model in self.csv_locations:
            pre_plots[model] = {}
            # For each csv
            for csv in self.csv_locations[model]:
                category = str()
                # Determine the column to reference
                category = 'Gender Key' if csv.lower().__contains__('gender') else category
                category = 'Employee Subgroup' if csv.lower().__contains__('employee') else category
                category = 'Personnel city' if csv.lower().__contains__('city') else category

                # Generate the unique values
                pre_plots[model][category] = {}
                for unique_value in self.master[model][csv][category].unique():
                    # ut.context(model + " " + str(unique_value))
                    pre_plots[model][category][unique_value] = self.master[model][csv][
                        self.master[model][csv][category] == unique_value]

        # Group the plots by date:
        self.plots = {}
        for model in pre_plots:
            self.plots[model] = {}
            for category in pre_plots[model]:
                self.plots[model][category] = {}
                for unique_value in pre_plots[model][category]:
                    self.plots[model][category][unique_value] = pre_plots[model][category][unique_value]
                    self.plots[model][category][unique_value] = self.plots[model][category][unique_value].groupby(
                        'Entry')
        ut.context(str(self.plots))

    def get_view(self):
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='diversity_model',
                    options=[{'label': i, 'value': i} for i in ['Original Data', 'Arima', 'Regression Analysis']],
                    multi=True,
                    value='Arima'
                ),
                dcc.Dropdown(
                    id='diversity_category',
                    options=[{'label': i, 'value': i} for i in ['Gender Key', 'Employee Subgroup', 'Personnel city']],
                    value='Gender Key'
                ),
                dcc.Dropdown(
                    id='diversity_unique_value_dropdown',
                    options=[{'label': i, 'value': i} for i in ['Male', 'Female']],
                    multi=True,
                    value='Male'
                ),

            ], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.RangeSlider(
                    id='date_slider',
                    min=min([int(group) for group in self.plots['Arima']['Gender Key']['Male'].groups]),
                    max=max([int(group) for group in self.plots['Arima']['Gender Key']['Male'].groups]),
                    value=[min([int(group) for group in self.plots['Arima']['Gender Key']['Male'].groups]),
                           max([int(group) for group in self.plots['Arima']['Gender Key']['Male'].groups])],
                    step=1,
                    allowCross=False,
                    marks=self.get_marks([int(group) for group in self.plots['Arima']['Gender Key']['Male'].groups])
                ),

            ], style={'margin-bottom': '20px', 'margin-left': '20px', 'width': '95%', 'align': 'center'}),

            dcc.Graph(id='diversity_trends')
        ], style={'margin-top': '10px','margin-bottom': '100px', 'color': 'black','background-color': 'rgb(0, 0, 0)'})

    def set_callbacks(self, app=dash.Dash()):
        @app.callback(Output('diversity_unique_value_dropdown', 'options'),
                      [Input('diversity_category', 'value'), Input('diversity_model', 'value')])
        def update_unique_value_dropdown(diversity_category, diversity_model):
            # Change the params to lists if they are strings
            if type(diversity_category) is str:
                diversity_category = [diversity_category]
            if type(diversity_model) is str:
                diversity_model = [diversity_model]

            return [{'label': i, 'value': i} for i in [unique_value for unique_value in
                                                       self.plots[diversity_model[0]][diversity_category[0]]]]

        @app.callback(Output('diversity_trends', 'figure'), [Input('diversity_model', 'value'),
                                                             Input('diversity_category', 'value'),
                                                             Input('diversity_unique_value_dropdown', 'value'),
                                                             Input('date_slider', 'value')])
        def update_trend_graph(diversity_model, diversity_category, diversity_unique_value_dropdown, date_slider):
            # Set starting variables
            data = []
            current_year = datetime.datetime.now().date().year - 2
            colors = plotly.colors.DEFAULT_PLOTLY_COLORS
            index = 0

            # Check param data types
            if type(diversity_model) is str:
                diversity_model = [diversity_model]
            if type(diversity_category) is str:
                diversity_category = [diversity_category]
            if type(diversity_unique_value_dropdown) is str:
                diversity_unique_value_dropdown = [diversity_unique_value_dropdown]
            if type(date_slider) is str:
                date_slider = [date_slider]

            # If original data is in the list of models to show
            # then put it in back so that the final color
            # is the original data set color
            if 'Original Data' in diversity_model:
                diversity_model.remove('Original Data')
                diversity_model.append('Original Data')

            for model in diversity_model:
                for category in diversity_category:
                    for unique_value in diversity_unique_value_dropdown:
                        # Set the x, y plots
                        x = []
                        y = []
                        name = unique_value
                        has_forecast = False

                        # Add the x and y, and convert the group nums to y
                        for group in self.plots[model][category][unique_value].groups:
                            # If the group is not in the range of values, skip
                            if int(group) not in range(date_slider[0], date_slider[1] + 1):
                                continue

                            x.append(group)
                            y.append(len(self.plots[model][category][unique_value].get_group(group).index))
                            # Add 'missing forecast' if the num of years
                            # is less than expected
                            if current_year <= int(group):  # TODO check
                                has_forecast = True
                                break

                        # Adding missing forecast if the has_forecast var is false
                        name = name + ': Missing forecast' if not has_forecast else name

                        # Add Scatter plot to data
                        data.append(Scatter(
                            x=x,
                            y=y,
                            name=str(model) + ' ' + name,
                            textfont=dict(
                                color='rgb(254, 165, 1)',
                            ),
                            mode='lines',
                            connectgaps=True,
                            line=dict(
                                color=colors[index],
                                width=4)
                        ))

                        # skip adding the forecast if there isnt one
                        if not has_forecast:
                            index = index + 1 if index < len(colors) else 0
                            continue

                        # Reset the x, y plots
                        x = []
                        y = []
                        # Add the x and y, and convert the group nums to y
                        for group in self.plots[model][category][unique_value].groups:
                            # If the group is not in the range of values, skip
                            if int(group) not in range(date_slider[0], date_slider[1]+1):
                                continue

                            if current_year <= int(group):
                                x.append(group)
                                y.append(len(self.plots[model][category][unique_value].get_group(group).index))

                        data.append(Scatter(
                            x=x,
                            y=y,
                            name=str(model) + ' ' + unique_value + ' forecast',
                            textfont=dict(
                                color='rgb(254, 165, 1)',
                            ),
                            mode='lines+markers',
                            connectgaps=True,
                            line=dict(
                                color=colors[index],
                                width=4),
                            marker= dict(
                                color=colors[index],
                                size=11)
                        ))

                        index = index + 1 if index < len(colors) else 0
            return Figure(data=data, layout=Layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        legend=dict(
                            traceorder='normal',
                            font=dict(
                                color='rgb(255, 255, 255)'
                            ),
                        ),
                        xaxis=dict(
                            tickfont=dict(
                                color='white'
                            ),
                        ),
                        yaxis=dict(
                            tickfont=dict(
                                color='white'
                            ),
                        )
                    )
                )


    def is_future(self, year):
        if year > datetime.datetime.now().year - 3:
            return 'rgb(254, 165, 1)'
        else:
            return 'rgb(136, 142, 147)'

    def get_marks(self, dates=list(), step=2):
        dates = sorted(dates)
        year_marks = {}
        index = 0
        for year in set(dates):
            if index % step == 0:
                year_marks[str(year)] = {'label': str(year), 'style': {'color': 'white', 'width': '30px',
                                                                       'background-color': self.is_future(year)}}
            else:
                year_marks[str(year)] = {'label': '',
                                         'style': {'color': 'white', 'width': '30px',
                                                   'background-color': self.is_future(year)}}
            index += 1
        return year_marks

    def get_page_id(self):
        return 'page__diversity_trends_new'

    def get_page_name(self):
        return 'Forecasts'
