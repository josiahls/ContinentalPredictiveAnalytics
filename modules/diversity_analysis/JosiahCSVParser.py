import typing

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
                              'UNCC My Success.csv']

        self.desired_columns = {'UNCC_Termination pre 2017': [
            'Personnel No.',
            'Job Title',
            'Employee Group',
            'Employee Subgroup',
            'Gender Key',
            'Ethnicity',
            'Termination',
            'Reason for action'
        ], 'UNCC_HR Master Data active employees': [
            'Personnel Number',
            'Job Title',
            'Employee Group',
            'Employee Subgroup',
            'Gender Key',
            'Pay scale type',
        ], 'UNCC My Success': [
            'Employee Id',
            'Gender',
            'Nationality',
            'Employee Group',
            'Employee Subgroup',
            'Position Title'
        ]}

        self.columns_to_rename = {
            'UNCC_Termination pre 2017': [{}
                                          ],
            'UNCC_HR Master Data active employees': [
                {'Employee Subgroup': 'Employee Pay Group'},
                {'Personnel Number': 'Personnel No.'}
            ],
            'UNCC My Success': [
                {'Employee Subgroup': 'Employee Pay Group'},
                {'Employee Id': 'Personnel No.'},
                {'Gender': 'Gender Key'},
            ]}

        self.master_csv = {}

    def load_CSVs(self, read_limit=None):
        for location in self.csv_locations:
            if location.__contains__('.xlsx'):
                data = pd.read_excel(self.data_workspace + location).iloc[:read_limit]
                new_data = pd.DataFrame(data=data)
                self.master_csv[location.split('.xlsx')[0]] = data
            if location.__contains__('.csv'):
                data = pd.read_csv(self.data_workspace + location, nrows=read_limit)
                self.master_csv[location.split('.csv')[0]] = data

        for key in self.master_csv:
            ut.context("Loaded data sheets: " + key)
            # Drop Columns that are not important

    def generate_CSV(self, show_limit=40):
        # For each csv file
        for label in self.master_csv:
            data_frame = pd.DataFrame(self.master_csv[label])
            # Drop the columns specified in desired_columns
            for key in data_frame:
                if key not in self.desired_columns[label]:
                    data_frame.drop(labels=key, axis=1, inplace=True)

            # Rename the columns specified in columns_to_rename
            if self.columns_to_rename[label]:
                for i in range(0, len(self.columns_to_rename[label])):
                    data_frame.rename(columns=self.columns_to_rename[label][i], inplace=True)

            self.master_csv[label] = data_frame
            # ut.context("Showing data frame after column rename fixes \n" + data_frame.head(show_limit).to_string())

        # Find min len so that a merge can happen
        minimum = min(len(self.master_csv[label]) for label in self.master_csv)

        # Merge All CSVs into one set
        self.master_csv['local'] = pd.DataFrame()
        for i, label in enumerate(self.master_csv):
            # ut.context("minimum is: " + str(minimum))
            if i != 0 and label != 'local':
                self.master_csv['local'] = pd.DataFrame(self.master_csv['local']).merge(
                    pd.DataFrame(self.master_csv[label].head(minimum - 1)), on='Personnel No.', sort=True, how='outer')
            elif i == 0:
                self.master_csv['local'] = pd.DataFrame(self.master_csv[label].head(minimum - 1))

        ut.context("Loaded data sheets: " + self.master_csv['local'].head(show_limit).to_string())
        pd.DataFrame(self.master_csv['local']).to_csv('josiah_local.csv')

if __name__ == '__main__':
    dp = JosiahCSVParser()
    dp.load_CSVs(read_limit=None)
    dp.generate_CSV()
