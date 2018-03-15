import os
from pathlib import Path

import numpy
import plotly.plotly as py
import plotly.graph_objs as go
from dash import Dash, dash
from core.module import Module
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import app


class DiversityModule(Module):
    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame()

        data_workspace = str(Path(__file__).parents[0])
        data_workspace += os.sep
        self.df = pd.read_csv(data_workspace + 'josiah_local.csv', encoding="ISO-8859-1")

    def get_module_name(self):
        return "Diversity"

    def get_tab_value(self):
        return "tab_diversity"

    def __str__(self):
        return "hello"

    def get_view(self):
        return html.Div([
            # Add the bar chart
            html.H1('Bar Comparisons'),
            dcc.Dropdown(
                id='axis_diversity_dropdown',
                options=[
                    {'label': label, 'value': label} for label in self.df
                ],
                value=list(self.df.columns.values)[2]
            ),
            dcc.Graph(id='diversity_bar_graph'),
            # Add the pie chart,
            html.H1('Pie Comparisons'),
            dcc.Dropdown(
                id='pie_labels_diversity_dropdown',
                options=[
                    {'label': label, 'value': label} for label in self.df
                ],
                value=list(self.df.columns.values)[2]
            ),
            dcc.Graph(id='diversity_pie_graph'),
            # Add the comparison bar chart
            html.H1('Bar Comparisons'),
            dcc.Dropdown(
                id='sample_1_axis_diversity_dropdown',
                options=[
                    {'label': label, 'value': label} for label in self.df
                ],
                value=list(self.df.columns.values)[2]
            ),
            dcc.Dropdown(
                id='sample_2_axis_diversity_dropdown',
                options=[
                    {'label': label, 'value': label} for label in self.df
                ],
                value=list(self.df.columns.values)[2]
            ),
            dcc.Graph(id='diversity_comparison_bar_graph')

        ])

    def set_callback_function(self, app=dash.Dash()):
        print("setting call backs for tab_diversity")

        @app.callback(Output('diversity_pie_graph', 'figure'), [Input('pie_labels_diversity_dropdown', 'value')])
        def update_chart(pie_labels_diversity_dropdown):
            print("Doing value update for  " + str(pie_labels_diversity_dropdown))

            # Get the value for the pie chart
            labels = self.df[pie_labels_diversity_dropdown].dropna()
            labels = labels.unique()
            # Get the number of occurances for each value
            values = [self.df[pie_labels_diversity_dropdown].value_counts()[label] for label in labels]
            return {
                'data': [
                    go.Pie(labels=labels, values=values)
                ]
                ,
                'layout': {'title': ('Pie Chart of: ' + pie_labels_diversity_dropdown)}
            }

        @app.callback(Output('diversity_bar_graph', 'figure'), [Input('axis_diversity_dropdown', 'value')])
        def update_graph(axis_diversity_dropdown):
            print("Doing value update for  " + str(axis_diversity_dropdown))
            # Get the value for the graph chart
            labels = self.df[axis_diversity_dropdown].dropna()
            labels = labels.unique()
            # Get the number of occurances for each value
            values = [self.df[axis_diversity_dropdown].value_counts()[label] for label in labels]

            print('Labels: ' + str(labels))
            print('Values: ' + str(values))

            return {
                'data': [
                    {'x': labels, 'y': values, 'type': 'bar'}
                ]
            }

        @app.callback(Output('diversity_comparison_bar_graph', 'figure'),
                      [Input('sample_1_axis_diversity_dropdown', 'value'),
                       Input('sample_2_axis_diversity_dropdown', 'value')])
        def update_graph(sample_1_axis_diversity_dropdown, sample_2_axis_diversity_dropdown):
            print("Doing value update for coutning bar " + str(sample_1_axis_diversity_dropdown))
            # Get the value for the pie chart
            labels = self.df[sample_1_axis_diversity_dropdown].dropna()
            labels = labels.unique()  # ex: male female
            # Get the value for the pie chart
            labels2 = self.df[sample_2_axis_diversity_dropdown].dropna()
            labels2 = labels2.unique()  # ex: other values

            print('Labels: ' + str(labels))
            # Get the number of occurances for each combination

            values_per_labels1 = {}
            for label in labels:
                for other in labels2:
                    # Get the rows of the values in one column compared to the other
                    rows = pd.DataFrame(self.df.loc[(self.df[sample_1_axis_diversity_dropdown] == label) &
                                                    (self.df[sample_2_axis_diversity_dropdown] == other)])
                    occurances = pd.DataFrame(rows).size

                    if label in values_per_labels1:
                        values_per_labels1[label].append(occurances)
                    else:
                        values_per_labels1[label] = numpy.ndarray(occurances, dtype=int)

            print('Values: ' + str(values_per_labels1))
            data = []
            for label in labels:
                for i, occurance in enumerate(values_per_labels1[label]):
                    data.append({'x': (str(label) + ': ' + labels2[i]),
                                 'y': occurance, 'type': 'bar'})

            return {
                'data': data
            }
