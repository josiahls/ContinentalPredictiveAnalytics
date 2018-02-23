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
            'Job',
            'Employee Group',
            'Employee Subgroup',
            'Gender Key',
            'Ethnicity',
            'Termination',
            'Reason for action'
        ], 'UNCC_HR Master Data active employees': [
            'Personnel Number',
            'Job',
            'Position',
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
                {'Personnel Number': 'Personnel No.'}
            ],
            'UNCC My Success': [
                {'Employee Id': 'Personnel No.'}
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

    def generate_CSV(self, show_limit=5):
        for label in self.master_csv:
            data_frame = pd.DataFrame(self.master_csv[label])
            # ut.context("Showing dataframe before editing \n" + data_frame.head(show_limit).to_string())
            # Drop columns that we dont want
            # ut.context(str(len(data_frame)))
            for key in data_frame:
                if key not in self.desired_columns[label]:
                    data_frame.drop(labels=key, axis=1, inplace=True)
            # ut.context("Showing dataframe after key drop \n" + data_frame.head(show_limit).to_string())
            # ut.context("\n")

            # Show Unique Values
            # for key in data_frame:
            #     ut.context("Show value occupancies: " + key + ": " + str(data_frame[key].unique()))

            if self.columns_to_rename[label]:
                for i in range(0, len(self.columns_to_rename[label])):
                    data_frame.rename(columns=self.columns_to_rename[label][i], inplace=True)

            ut.context("Showing dataframe after column rename fixes \n" + data_frame.head(show_limit).to_string())


if __name__ == '__main__':
    dp = JosiahCSVParser()
    dp.load_CSVs(read_limit=10)
    dp.generate_CSV(300)
