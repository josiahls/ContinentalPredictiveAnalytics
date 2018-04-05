import pandas as pd
import os
import numpy as np
from util.utility import Utility
from pathlib import Path
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

from matplotlib import pyplot as plt



# noinspection PyUnusedLocal,PyPep8Naming
class Ramya_DiversityPrediction(object):
    def __init__(self):
        self.data = {}
        self.data_workspace = str(Path(__file__).parents[0])
        self.data_workspace += os.sep

        self.Pred = pd.read_excel(self.data_workspace + 'RamyaCleanedDiversity.xlsx', encoding='ISO-8859-1')

        #print(self.Pred.head())

        self.Years_based_columns = ['Entry','Gender Key','Latitude','Longitude'];

        self.Pred['Entry'] = pd.to_datetime(self.Pred['Entry'])

        self.Pred['Entry'] = self.Pred['Entry'].apply(lambda x: x.strftime('%m-%Y'))



        print(self.Pred.head())

        #self.Pred['Entry'] = self.Pred['Entry'].dt.strftime('%Y-%m-%d')


        #df2 = pd.DataFrame(self.Pred['Entry'].str.split('-', 2).tolist(),
                           #columns=['Hire Year','Hire Month','b'])



        #self.Pred = pd.concat([self.Pred, df2], axis=1)

        #self.Pred['Hire Year']= self.Pred['Hire Year'].astype(str)  + self.Pred['Hire Month']

        self.Pred = self.Pred[self.Years_based_columns]

        print(self.Pred.head())

        #self.diversity = self.diversity[pd.notnull(self.diversity['Gender Key'])]


        self.df= self.Pred.groupby(['Entry','Gender Key'], as_index=False).count()

        #self.df.columns =['_'.join(x) for x in self.df.columns.ravel()]

        print(self.df.head(15))












if __name__ == '__main__':
    dp = Ramya_DiversityPrediction()