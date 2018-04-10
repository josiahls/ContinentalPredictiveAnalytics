import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import dash
from pathlib import Path
import os
from dash.dependencies import Input, Output
from core.view import View
from util.utility import Utility
import pandas as pd
import numpy as np

ut = Utility('UnitedStatesMapView')


class UnitedStatesMapView(View):
    def __init__(self, name=str, data=pd.DataFrame):
        super().__init__(name=name, data=pd.DataFrame)
        self.name = name
        self.unique_values = {}
        self.global_unique_values = {}
        self.current_category = str
        self.data = data
        self.filtered_values = pd.DataFrame

    def setFields(self, category=None, unique_values=None):
        # Set the categories
        if category is None:
            category = self.current_category
        else:
            self.current_category = category
        # Set the unique values
        if unique_values is None:
            self.unique_values = self.unique_values
        elif type(unique_values) is list:
            if 'all' in unique_values:
                self.unique_values = self.global_unique_values[category]
            else:
                self.unique_values = unique_values
        elif type(unique_values) is str:
            if unique_values.__contains__('all'):
                self.unique_values = self.global_unique_values[category]
            else:
                self.unique_values = [unique_values]
        else:
            self.global_unique_values = unique_values
            self.unique_values = self.global_unique_values[category]

        # Set the filtered values
        # Filter the rows by whether they contain the values
        # specified
        self.filtered_values = self.data[
            self.data[category].isin(self.unique_values)]

    def get_view(self):
        # For each unique value, get the max value for normalizing
        normalized_max = pd.DataFrame(self.filtered_values).groupby(['Latitude', 'Longitude'])[self.current_category].count().max()

        locations = []
        for unique_value in self.unique_values:
            # Get the rows containing that value
            rows_for_unique_value = self.filtered_values[self.filtered_values[self.current_category] == unique_value]
            value_groups = pd.DataFrame(rows_for_unique_value).groupby(['Latitude', 'Longitude', 'Location.Name'],
                                                                       as_index=False).count()

            # Count the number of unique values at a matching lat and long
            # ut.context(str(value_groups))
            ut.context(str(rows_for_unique_value.count()))
            ut.context(str(value_groups.count()))

            location = {}
            for i in range(0, value_groups[self.current_category].count()):
                ut.context(str(value_groups['Longitude'].iloc[[i]]))
                if value_groups['Longitude'].iloc[i] > 30 or value_groups['Latitude'].iloc[i] < 10:
                    continue

                location = dict(
                    type='scattergeo',
                    locationmode='USA-states',
                    lon=value_groups['Longitude'].iloc[[i]],
                    lat=value_groups['Latitude'].iloc[[i]],
                    text=str(self.current_category) + ' - {}'.format(unique_value) + ': ' +
                         '{} units<br>'.format(value_groups[self.current_category].iloc[i]),
                    mode='markers',
                    marker=dict(
                        size=value_groups[self.current_category].iloc[i] / normalized_max * 100,
                        opacity=0.8,
                        reversescale=True,
                        autocolorscale=False,
                        symbol='circle',
                        line=dict(
                            width=1,
                            color='rgba(102, 102, 102)'
                        ),
                    ),
                    name=str(value_groups['Location.Name'].iloc[i]) + ' ' +
                         '{} units<br>'.format(value_groups[self.current_category].iloc[i]) + ' {}'.format(unique_value)
                )
                ut.context(str(value_groups['Location.Name'].iloc[[i]]))
                locations.append(location)

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

        fig = dict(data=locations, layout=layout)
        return fig

    def set_callbacks(self, app=dash.Dash()):
        @app.callback(Output(self.get_graph_id(), 'figure'), [Input('category_dropdown', 'value'),
                                                                Input('unique_value_dropdown', 'value')])
        def update_chart(category_dropdown, unique_value_dropdown):
            self.setFields(category=category_dropdown, unique_values=unique_value_dropdown)
            return self.get_view()

    def get_graph_id(self):
        return str('diversity_map_graph')