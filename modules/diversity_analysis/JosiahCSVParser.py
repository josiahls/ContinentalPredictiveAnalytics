import pandas as pd
import os
from util.utility import Utility
from pathlib import Path

ut = Utility('JosiahCSVParser')


class JosiahCSVParser(object):
    """
    Loads and parses:
    UNCC Termination pre 2017
    UNCC_HR Master Data active employees
    UNCC My Success
    MFG10YearTerminationData
    """

    def __init__(self):
        self.data = {}
        self.data_workspace = str(Path(__file__).parents[2])
        self.data_workspace += os.sep + 'misc' + os.sep

        ut.context(self.data_workspace)
        self.csv_locations = ['UNCC_Termination pre 2017.xlsx',
                              'UNCC_HR Master Data active employees.xlsx',
                              'UNCC My Success.csv',
                              'MFG10YearTerminationData.csv']
        self.master_csv = {}

    def load_CSVs(self, read_limit=None):
        for location in self.csv_locations:
            if location.__contains__('.xlsx'):
                data = pd.read_excel(self.data_workspace + location).iloc[:read_limit]
                self.master_csv[location.split('.xlsx')[0]] = data
            if location.__contains__('.csv'):
                data = pd.read_csv(self.data_workspace + location, nrows=read_limit)
                self.master_csv[location.split('.csv')[0]] = data

        for key in self.master_csv:
            ut.context("Loaded data sheets: " + key)

    def generate_CSV(self):

        for key in self.master_csv['UNCC_Termination pre 2017']:
            ut.context(key)



        pass


if __name__ == '__main__':
    dp = JosiahCSVParser()
    dp.load_CSVs(read_limit=10)
    dp.generate_CSV()
