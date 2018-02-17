from abc import ABC, abstractmethod


class Module(ABC):
    def __init__(self):
        """
        This is the core module. One of the main functions of it is to
        return a view that dash can handle.
        """
        pass

    @abstractmethod
    def get_view(self):
        pass

    @abstractmethod
    def get_module_name(self):
        pass

    @abstractmethod
    def get_tab_value(self):
        pass

    @abstractmethod
    def __str__(self):
        pass