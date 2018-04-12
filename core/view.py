from abc import ABC, abstractmethod
import dash
import pandas


class View(ABC):
    def __init__(self, name=str, data=pandas.DataFrame):
        """
        This is the core module. One of the main functions of it is to
        return a view that dash can handle.
        """

    @abstractmethod
    def get_view(self):
        pass

    @abstractmethod
    def set_callbacks(self, app=dash.Dash()):
        pass

    @abstractmethod
    def get_graph_id(self):
        pass
