import os
from pathlib import Path

import pandas as pd

data_workspace = str(Path(__file__).parents[0])
data_workspace += os.sep

print(data_workspace + 'josiah_local.csv')
# df = pd.read_csv(data_workspace + 'josiah_local.csv', encoding = "ISO-8859-1")
#
# label_col = df.columns.values[4]
# print(str(list(label_col)))
# print(str(list(df[label_col].unique())))
#
# # Get the value for the pie chart
# labels = df[label_col].dropna()
# labels = labels.unique()
# # Get the number of occurances for each value
# values = [df[label_col].value_counts()[label] for label in labels]
#
# print(str(labels))
# print(str(values))
#
# labels = self.df[sample_1_axis_diversity_dropdown].dropna()
# labels = labels.unique()  # ex: male female
# # Get the value for the pie chart
# labels2 = self.df[sample_2_axis_diversity_dropdown].dropna()
# labels2 = labels2.unique()  # ex: other values
#
# print('Labels: ' + str(labels))

df = pd.DataFrame(pd.read_csv(data_workspace + 'josiah_local.csv', encoding = "ISO-8859-1"))

label_col = df.columns.values[4]
label_col2 = df.columns.values[6]

labels = df[label_col].dropna()
labels = labels.unique()  # ex: male female
# Get the value for the pie chart
labels2 = df[label_col2].dropna()
labels2 = labels2.unique()  # ex: other values

values = []
data = []
print(str(label_col) + " " + str(label_col2))

multi_row = {}
for label in labels:
    for other in labels2:
        rows = pd.DataFrame(df.loc[(df[label_col] == label) & (df[
            label_col2] == other)])
        occurances = pd.DataFrame(rows).size
        if not rows.empty:
            if label in multi_row and not pd.DataFrame(multi_row[label]).empty:
                multi_row[label].append(rows)
            else:
                multi_row[label] = rows

print(str(multi_row))
for row in multi_row:
    print('\n\n')
    for i, single_set in enumerate(row):
        print(pd.DataFrame(multi_row[row]).size)


