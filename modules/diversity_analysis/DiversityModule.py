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
    def __init__(self, data_workspace=None):
        super().__init__()
        self.df = pd.DataFrame()

        if data_workspace is None:
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
        test_trace = pd.DataFrame()
        test_trace['numeric_axis'] = [i for i in range(2010, 2025, 1)]


        # test_trace = go.Scatter(x=[i for i in range(100)],
        #                    y=[i*numpy.random.randint(1, 100) for i in range(100)])

        # Build map
        data = [dict(
            type='scattergeo',
            locationmode='USA-states',
        )]

        layout = dict(
            title='Diversity Map',
            colorbar=True,
            geo=dict(
                scope='usa',
                projection=dict(type='albers usa'),
                showland=True,
                # landcolor="rgb(250, 250, 250)",
                landcolor="rgb(105,105,105)",
                # subunitcolor="rgb(217, 217, 217)",
                subunitcolor="white",
                countrycolor="rgb(217, 217, 217)",
                countrywidth=0.5,
                subunitwidth=0.5
            ),
            height=800,

        )

        fig = dict(data=data, layout=layout)

        return html.Div([
            html.Div([
                html.Div([
                    html.H3('Gender'),
                    dcc.Dropdown(
                        id='crossfilter-xaxis-column',
                        options=[{'label': i, 'value': i} for i in ['female', 'male']],
                        value='female'
                    ),
                ],
                    style={'width': '49%', 'display': 'inline-block', 'padding' : '0px'}),

                html.Div([

                    html.H3('Values'),
                    dcc.Dropdown(
                        options=[{'label': i, 'value': i} for i in ['value', 'other value', 'other other value']],
                        multi=True,
                        value="value"
                    ),
                ],
                    style={'width': '49%', 'display': 'inline-block', }),
            ],                    style={'width': '100%', 'display': 'inline-block', },

            ),

            html.H3('Unit Options'),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Numeric', 'Ratio']],
                value='Numeric',
                # labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(id='diversity_map_graph', figure=fig),
            html.Div([
                html.H3('Year'),
                dcc.RangeSlider(
                    id='my-range-slider',
                    min=test_trace['numeric_axis'].min(),
                    max=test_trace['numeric_axis'].max(),
                    value=[test_trace['numeric_axis'].min(),test_trace['numeric_axis'].max()],
                    step=None,
                    marks={str(year): {'label': str(year),'style': {'color': 'white', 'background-color': 'rgb(135,206,250)'  }} for year in test_trace['numeric_axis'].unique()},),

             ],style={'margin-left': '10px','width': '95%', 'align':'center'}),
        ])

    def set_callback_function(self, app=dash.Dash()):
        pass

    # def get_view(self):
    #     return html.Div([
    #         # Add the bar chart
    #         html.H1('Bar Comparisons'),
    #         dcc.Dropdown(
    #             id='axis_diversity_dropdown',
    #             options=[
    #                 {'label': label, 'value': label} for label in self.df
    #             ],
    #             value=list(self.df.columns.values)[2]
    #         ),
    #         dcc.Graph(id='diversity_bar_graph'),
    #         # Add the pie chart,
    #         html.H1('Pie Comparisons'),
    #         dcc.Dropdown(
    #             id='pie_labels_diversity_dropdown',
    #             options=[
    #                 {'label': label, 'value': label} for label in self.df
    #             ],
    #             value=list(self.df.columns.values)[2]
    #         ),
    #         dcc.Graph(id='diversity_pie_graph'),
    #         # Add the comparison bar chart
    #         html.H1('2 Column Comparisons'),
    #         dcc.Dropdown(
    #             id='sample_1_axis_diversity_dropdown',
    #             options=[
    #                 {'label': label, 'value': label} for label in self.df
    #             ],
    #             value=list(self.df.columns.values)[2]
    #         ),
    #         dcc.Dropdown(
    #             id='sample_2_axis_diversity_dropdown',
    #             options=[
    #                 {'label': label, 'value': label} for label in self.df
    #             ],
    #             value=list(self.df.columns.values)[2]
    #         ),
    #         dcc.Graph(id='diversity_comparison_bar_graph')
    #
    #     ])
    #
    # def set_callback_function(self, app=dash.Dash()):
    #     print("setting call backs for tab_diversity")
    #
    #     @app.callback(Output('diversity_pie_graph', 'figure'), [Input('pie_labels_diversity_dropdown', 'value')])
    #     def update_chart(pie_labels_diversity_dropdown):
    #         print("Doing value update for  " + str(pie_labels_diversity_dropdown))
    #
    #         # Get the value for the pie chart
    #         labels = self.df[pie_labels_diversity_dropdown].dropna()
    #         labels = labels.unique()
    #         # Get the number of occurances for each value
    #         values = [self.df[pie_labels_diversity_dropdown].value_counts()[label] for label in labels]
    #         return {
    #             'data': [
    #                 go.Pie(labels=labels, values=values)
    #             ]
    #             ,
    #             'layout': {'title': ('Pie Chart of: ' + pie_labels_diversity_dropdown)}
    #         }
    #
    #     @app.callback(Output('diversity_bar_graph', 'figure'), [Input('axis_diversity_dropdown', 'value')])
    #     def update_graph(axis_diversity_dropdown):
    #         print("Doing value update for  " + str(axis_diversity_dropdown))
    #         # Get the value for the graph chart
    #         labels = self.df[axis_diversity_dropdown].dropna()
    #         labels = labels.unique()
    #         # Get the number of occurances for each value
    #         values = [self.df[axis_diversity_dropdown].value_counts()[label] for label in labels]
    #
    #         print('Labels: ' + str(labels))
    #         print('Values: ' + str(values))
    #
    #         return {
    #             'data': [
    #                 {'x': labels, 'y': values, 'type': 'bar'}
    #             ]
    #         }
    #
    #     @app.callback(Output('diversity_comparison_bar_graph', 'figure'),
    #                   [Input('sample_1_axis_diversity_dropdown', 'value'),
    #                    Input('sample_2_axis_diversity_dropdown', 'value')])
    #     def update_graph(sample_1_axis_diversity_dropdown, sample_2_axis_diversity_dropdown):
    #         print("Doing value update for coutning bar " + str(sample_1_axis_diversity_dropdown))
    #         # Get the value for the pie chart
    #         labels = self.df[sample_1_axis_diversity_dropdown].dropna()
    #         labels = labels.unique()  # ex: male female
    #         # Get the value for the pie chart
    #         labels2 = self.df[sample_2_axis_diversity_dropdown].dropna()
    #         labels2 = labels2.unique()  # ex: other values
    #
    #         # print('Labels: ' + str(labels))
    #         # Get the number of occurances for each combination
    #
    #         values_per_labels1 = {}
    #         for label in labels:
    #             for other in labels2:
    #                 # Get the rows of the values in one column compared to the other
    #                 rows = pd.DataFrame(self.df.loc[(self.df[sample_1_axis_diversity_dropdown] == label) &
    #                                                 (self.df[sample_2_axis_diversity_dropdown] == other)])
    #
    #                 # print(str(rows))
    #                 occurances = pd.DataFrame(rows).shape[0]
    #
    #                 if label in values_per_labels1:
    #                     values_per_labels1[label].append(occurances)
    #                 else:
    #                     values_per_labels1[label] = [occurances]
    #
    #         # print('Values: ' + str(values_per_labels1))
    #         data = []
    #         index = 0
    #         final_labels = []
    #         final_axis = []
    #         for label in labels:
    #             for i, occurance in enumerate(values_per_labels1[label]):
    #                 # if occurance != 0:
    #                 final_labels.append((str(label) + '_' + labels2[i]))
    #                 final_axis.append(occurance)
    #                 # data.append({'x': (str(label) + '_' + labels2[i]),
    #                 #              'y': occurance, 'type': 'bar'})
    #                 # index += 1
    #                 # data.append({'x': index,
    #                 #              'y': occurance, 'type': 'bar'})
    #
    #         print(str(data))
    #         return {
    #             # 'data': [data]
    #             'data': [{'x': final_labels,
    #                       'y': final_axis, 'type': 'bar'}]
    #         }
