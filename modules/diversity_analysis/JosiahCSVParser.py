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
                              'UNCC My Success.csv']

        self.desired_columns = {'UNCC_Termination pre 2017': [
            'Personnel No.',
            'Job Title',
            'Employee Group',
            'Employee Subgroup',
            'Gender Key',
            'Entry'
            'Birth Date',
            'Ethnicity',
            'Termination',
            'Personnel Area',
            'Reason for action'
        ], 'UNCC_HR Master Data active employees': [
            'Personnel Number',
            'Job Title',
            'Employee Group',
            'Employee Subgroup',
            'Gender Key',
            'Personnel Area'
            'Pay scale type',
        ], 'UNCC My Success': [
            'Employee Id',
            'Hire Date',
            'Date of Birth',
            'Gender',
            'Nationality',
            'Employee Group',
            'Personnel Area',
            'Employee Subgroup',
            'Position Title'
        ]}

        self.columns_to_rename = {
            'UNCC_Termination pre 2017': [{'Employee Subgroup': 'Employee Pay Group'},
                                          {'Entry':'Hire Date'}
                                          ],
            'UNCC_HR Master Data active employees': [
                {'Employee Subgroup': 'Employee Pay Group'},
                {'Personnel Number': 'Personnel No.'}
            ],
            'UNCC My Success': [
                {'Employee Subgroup': 'Employee Pay Group'},
                {'Employee Id': 'Personnel No.'},
                {'Gender': 'Gender Key'},
                {'Date of Birth': 'Birth Date'},
            ]}

        self.internal_columns_to_merge = {
            'Gender Key': [],
            'Job Title': ['Position Title'],
            'Employee Group': [],
            'Employee Pay Group': []
        }

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

                self.master_csv['local']['Gender Key'].replace(['M', 'F'], ['Male', 'Female'], inplace=True)


if __name__ == '__main__':
    dp = JosiahCSVParser()
    dp.load_CSVs(read_limit=10)
    dp.generate_CSV()
