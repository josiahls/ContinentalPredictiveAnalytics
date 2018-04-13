import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import dash
from pathlib import Path
import os
from dash.dependencies import Input, Output
from core.module import Module
from util.utility import Utility
import numpy as np

from core import Page

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

        self.csv_locations = ['master.csv', 'code_table.csv']

    def get_view(self):
        return html.Div([
            html.Div([
                html.H3('Categories')]),
        ])

    def set_callbacks(self, app=dash.Dash()):
        pass

    def get_page_id(self):
        return 'page__diversity_trends'

    def get_page_name(self):
        return 'Trends'