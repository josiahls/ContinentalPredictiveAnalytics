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



# Cross validation with Linear Regression to check the accuracy

class Ramya_Liner_Regression(object):
    def __init__(self):
        self.data = {}
        self.data_workspace = str(Path(__file__).parents[0])
        self.data_workspace += os.sep

        self.Pred = pd.read_excel(self.data_workspace + 'ARIMA_Female.xlsx', encoding='ISO-8859-1')

        #print(self.Pred.head())

        #self.Years_based_columns = ['Entry','Gender Key','Latitude','Longitude','Hire Year'];

        #self.Pred['Entry'] = pd.to_datetime(self.Pred['Entry'], format='%Y')

        #my_date = pd.to_datetime(date, format='%Y%m%d')

        #self.Pred['Entry'] = pd.to_string(self.Pred['Entry'])

        """ print(self.Pred.head())

        self.Pred['Entry'] = self.Pred['Entry'].dt.strftime('%Y-%m-%d')


        df2 = pd.DataFrame(self.Pred['Entry'].str.split('-', 2).tolist(),
                           columns=['Hire Year','a','b'])

        self.Pred = pd.concat([self.Pred, df2], axis=1)

        self.Pred = self.Pred[self.Years_based_columns]

        print(self.Pred.head())

        #self.diversity = self.diversity[pd.notnull(self.diversity['Gender Key'])]

        self.Pred["Gender Key"] = self.Pred["Gender Key"].astype('category')
        self.Pred.dtypes

        self.Pred["Gender Key_ENC"] = self.Pred["Gender Key"].cat.codes

        self.diversity["Employee Pay Group"] = self.diversity["Employee Pay Group"].astype('category')
        self.diversity.dtypes

        self.diversity["Employee Pay Group_ENC"] = self.diversity["Employee Pay Group"].cat.codes

        print(self.diversity.head())

        # self.feature_names = ["Gender Key_ENC ","Job Title_ENC"]

        # diversity_imputer = pd.DataFrame(self.diversity, columns=self.feature_names)

        # print(diversity_imputer.head())

        # target = pd.DataFrame(self.diversity.target, columns=["Gender Key_ENC"])"""

        X = np.array(self.Pred['Entry']).reshape(-1, 1)
        y = np.array(self.Pred['Female']).reshape(-1, 1)

        # print(X)
        #       y = self.diversity["Gender Key_ENC"]

        # y = y.to_string(index=False)
        # print(str(np.array(X).shape))
        # print(str(np.array(y).shape))

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        print(len(X))
        print(len(y))

        lm = linear_model.LinearRegression()
        print(str(np.array(X_train).shape))
        print(str(np.array(y_train).shape))

        model = lm.fit(X_train, y_train)
        predictions = lm.predict(X_test)

        plt.scatter(y_test, predictions)
        plt.xlabel('True Values')
        plt.ylabel('Predictions')

        print('Score:', model.score(X_test, y_test))



if __name__ == '__main__':
    dp = Ramya_Liner_Regression()

