import dash
import pandas as pd
import datetime as dt

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
            if year > dt.datetime.now().year:
                return 'rgb(0,250,0)'
            else:
                return 'rgb(135,206,250)'

        def get_marks():
            year_marks = {}
            for year in set(self.date_range):
                year_marks[str(year)] = {'label': str(year),'style': {'color': 'white', 'background-color': is_future(year)}}
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

        ], style={'margin-bottom': '20px', 'width': '95%', 'align': 'center'})

    def set_callbacks(self, app=dash.Dash()):
        pass


    def get_graph_id(self):
        return 'date_slider'
