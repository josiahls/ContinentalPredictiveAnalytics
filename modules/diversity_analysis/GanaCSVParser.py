import pandas as pd
import os
from util.utility import Utility
from pathlib import Path

ut = Utility('GanaCSVParser')


class GanaCSVParser(object):
    """
    Loads and parses:
    UNCC Termination pre 2017
    UNCC_HR Master Data active employees
    UNCC My Success
    MFG10YearTerminationData
    """

    def __init__(self): # constructor
        self.data = {}
        self.data_workspace = str(Path(__file__).parents[2]) # to till the current directory and go 2 parents up
        self.data_workspace += os.sep + 'misc' + os.sep  #os.sep to go into the path to misc

        ut.context(self.data_workspace) # ut.cotext is same as print - by josiah
        self.csv_locations = ['UNCC_Termination pre 2017.xlsx',
                              'UNCC_HR Master Data active employees.xlsx',
                              'UNCC My Success.csv',
                              'MFG10YearTerminationData.csv']
        self.master_csv = {} # {} implies its dictionary(similar to hash map) and its empty

    def load_CSVs(self, read_limit=None):
        for location in self.csv_locations:
            if location.__contains__('.xlsx'):
                data = pd.read_excel(self.data_workspace + location).iloc[:read_limit] # pd : pandas
                self.master_csv[location.split('.xlsx')[0]] = data # select the 0th index value
            if location.__contains__('.csv'):
                data = pd.read_csv(self.data_workspace + location, nrows=read_limit)
                self.master_csv[location.split('.csv')[0]] = data

        for key in self.master_csv:
            ut.context("Loaded data sheets: " + key)

    def generate_CSV(self):
        #one csv  , save it in current directory.
        # drop unnecessary columns
        # make versions
        # fill missing data - like female is F

        for key in self.master_csv['UNCC_Termination pre 2017']:
            ut.context(key)



        pass


if __name__ == '__main__':
    dp = GanaCSVParser()
    dp.load_CSVs(read_limit=10)
    dp.generate_CSV()
