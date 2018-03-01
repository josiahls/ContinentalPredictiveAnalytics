import typing

import pandas as pd
import os
from util.utility import Utility
from pathlib import Path

ut = Utility('JosiahCSVParser')


# noinspection PyUnusedLocal,PyPep8Naming
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
                new_data = pd.DataFrame(data=data)
                self.master_csv[location.split('.xlsx')[0]] = data
            if location.__contains__('.csv'):
                data = pd.read_csv(self.data_workspace + location, nrows=read_limit)
                self.master_csv[location.split('.csv')[0]] = data

        for key in self.master_csv:
            ut.context("Loaded data sheets: " + key)
            # Drop Columns that are not important

    def generate_CSV(self, show_limit=10):
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
                    pd.DataFrame(self.master_csv[label].head(minimum - 1)), suffixes=['_1', '_2'], on='Personnel No.',
                    sort=True, how='outer')
            elif i == 0:
                self.master_csv['local'] = pd.DataFrame(self.master_csv[label].head(minimum - 1))

        # merge internal columns
        # ut.context("Loaded data sheets: " + self.master_csv['local'].head(show_limit).to_string())
        self.merge_internal_columns()
        ut.context("Loaded data sheets: " + self.master_csv['local'].head(show_limit).to_string())
        pd.DataFrame(self.master_csv['local']).to_csv('josiah_local.csv')

    def merge_internal_columns(self):
        # rename duplicate columns - might not need
        # cols = pd.Series(self.master_csv['local'].columns)
        # for dup in self.master_csv['local'].columns.get_duplicates(): cols[
        #     self.master_csv['local'].columns.get_loc(dup)] = [
        #     dup + '.' + str(d_idx) if d_idx != 0 else dup for d_idx in
        #     range(self.master_csv['local'].columns.get_loc(dup).sum())]
        # self.master_csv['local'].columns = cols

        # For each column to merge
        for column_to_merge in self.internal_columns_to_merge:
            # check the columns in the data frame
            column_list = set()

            # Add pre loaded columns
            if self.internal_columns_to_merge[str(column_to_merge)]:
                for value in self.internal_columns_to_merge[str(column_to_merge)]:
                    column_list.add(value)
            else:
                ut.context("List is empty")

            other_columns_found = False
            for column in pd.DataFrame(self.master_csv['local']):
                # if there is a match, then add to list of columns to merge
                if str(column).__contains__(column_to_merge) and str(column) != column_to_merge:
                    column_list.add(str(column))
                    other_columns_found = True

            if column_to_merge in pd.DataFrame(self.master_csv['local']):
                pass
            else:
                print("making empty column for  " + column_to_merge)
                self.master_csv['local'][column_to_merge] = pd.np.NaN
                other_columns_found = False

            # If there are not columns that match, then create a new one and merge similar columns
            if not other_columns_found:
                # Make an empty column
                for column in pd.DataFrame(self.master_csv['local']):
                    # If there is a similar column, then add to list of columns to merge
                    stripped_column = str(column).split('_')[0]
                    if str(column) not in self.internal_columns_to_merge \
                            and (str(column).__contains__(column_to_merge) or str(stripped_column).__contains__(
                                column_to_merge)):
                        column_list.add(str(column))
                        other_columns_found = True

            # try to replace nan values with corresponding columns
            for column in column_list:
                for i in range(0, len(pd.DataFrame(self.master_csv['local'][column]))):
                    if not pd.isnull(self.master_csv['local'].loc[i, column]):
                        self.master_csv['local'].loc[i, column_to_merge] = self.master_csv['local'].loc[i, column]

                # ut.context("Loaded data sheets: for " + column + " " + self.master_csv['local'].head(10).to_string())
                self.master_csv['local'] = pd.DataFrame(self.master_csv['local']).drop(column, 1)
                # ut.context("Loaded data sheets: for " + column + " "  + self.master_csv['local'].head(10).to_string())
                # ut.context("\n\n\n")

                # go through all the rows for empty columns
                # for i in range(1, len(pd.DataFrame(self.master_csv['local']))):
                #     if self.master_csv['local'][column_to_merge][i] is pd.np.NaN:
                #         changed = False
                #         # if the main column is null, see if there is another column with a value
                #         for column in column_list:
                #             # if there is, then use that value
                #             if self.master_csv['local'][column][i] is not pd.np.NaN:
                #                 self.master_csv['local'][column_to_merge][i] = self.master_csv['local'][column][i]
                #                 changed = True
                #                 break


if __name__ == '__main__':
    dp = JosiahCSVParser()
    dp.load_CSVs(read_limit=None)
    dp.generate_CSV()
