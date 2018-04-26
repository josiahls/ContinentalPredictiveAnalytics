import dash
import pandas as pd
import datetime

from core import View
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


class DateSlider(View):
    def __init__(self, name=str, data=pd.DataFrame):
        """
        This is the core module. One of the main functions of it is to
        return a view that dash can handle.
        """
        super().__init__(name, data)
        self.date_range=[]

    def set_fields(self, date_range):
        self.date_range = date_range

    def get_view(self):
        def is_future(year):
            if year > datetime.datetime.now().year - 2:
                return 'rgb(254, 165, 1)'
            else:
                return 'rgb(136, 142, 147)'

        def get_marks():
            year_marks = {}
            index = 0
            step = 2
            for year in set(self.date_range):
                if index % step == 0:
                    year_marks[str(year)] = {'label': str(year), 'style': {'color': 'white', 'width': '30px',
                                                                           'background-color': is_future(year)}}
                else:
                    year_marks[str(year)] = {'label': '',
                                             'style': {'color': 'white', 'width': '30px',
                                                       'background-color': is_future(year)}}
                index += 1
            return year_marks


        return html.Div([
            html.H3('Year'),
            dcc.RangeSlider(
                id='date_slider',
                min=min(self.date_range),
                max=max(self.date_range),
                value=[min(self.date_range), max(self.date_range)],
                step=2,
                # marks={'1696': {'label': str(1696), 'style': {'color': 'white', 'background-color': is_future(1696)}}}
                marks=get_marks()
            ),

        ], style={'margin-bottom': '20px','margin-left': '20px', 'width': '95%', 'align': 'center', 'color': 'rgb(254, 165, 1)'})

    def set_callbacks(self, app=dash.Dash()):
        pass


    def get_graph_id(self):
        return 'date_slider'
