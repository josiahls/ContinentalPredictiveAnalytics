import pandas as pd
import os
import numpy as np
from pathlib import Path
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
import warnings

warnings.filterwarnings("ignore")


# noinspection PyUnusedLocal,PyPep8Naming
class ARIMA_Coordinates(object):


    def __init__(self):
        self.data = {}
        self.data_workspace = str(Path(__file__).parents[0])
        self.data_workspace += os.sep

        self.Pred = pd.read_excel(self.data_workspace + 'CleanedDiversity_Coordinates.xlsx', encoding='ISO-8859-1')

        #pd.DataFrame(self.Pred).to_csv()

        print(self.Pred.tail())

        self.Years_based_columns = ['Entry', 'Gender Key', 'Coordinates'];

        self.Pred = self.Pred[self.Years_based_columns]

        self.Pred = self.Pred[self.Pred['Coordinates'] != '29.7606,-95.3697']

        self.Pred = self.Pred[self.Pred['Coordinates'] != '32.2216,-110.9698']

        self.Pred['Entry'] = self.Pred['Entry'].apply(lambda x: x.strftime('%Y'))

        columns = []
        for label in self.Pred:
            columns.append(label)
        latlong_Coord = []
        latlong_Coord = self.Pred['Coordinates'].unique()
        latlong_Coord.sort()
        '''lat_Coord =[]
        lat_Coord = [i.split(',', 1)[0] for i in latlong_Coord]
        long_Coord = []
        long_Coord = [i.split(',', 1)[1] for i in latlong_Coord]'''

        Coordinates_list = range(0, 34)

        for i in Coordinates_list:


            self.df = self.Pred.groupby(['Entry', 'Coordinates']).count()  # Grouping the Gender based on the month-year

            self.df1 = self.df.unstack('Coordinates')  # Display Gender values in seperate columns

            self.df1 = pd.DataFrame(self.df1, dtype='float')

            self.df1.fillna(self.df1.mean(), inplace=True)

            self.df1.drop(self.df1.index[:40], inplace=True)

            self.df1 = self.df1[self.df1.columns[i]]

            #self.df1.drop(self.df1.columns[i], axis=1, inplace=True)


            X = self.df1.values

            #self.df1.plot()

            #pyplot.show()

            #Refernece: https://machinelearningmastery.com/grid-search-arima-hyperparameters-with-python/

            split_point = len(self.df1) - 7

            dataset, validation = self.df1[0:split_point], self.df1[split_point:]

            print('Dataset %d, Validation %d' % (len(dataset), len(validation)))

            # Make the dataset stationary

            def difference(dataset, interval=1):
                diff = list()
                for i in range(interval, len(dataset)):
                    value = dataset[i] - dataset[i - interval]
                    diff.append(value)
                return np.array(diff)

            # Invert the differnced value

            def inverse_difference(history, yhat, interval=1):
                return yhat + history[-interval]

            differenced = difference(X)

            # Arima model, Coodinates calucalted by considering MSE

            model = ARIMA(differenced, order=(0, 2, 1))

            model_fit = model.fit(disp=0)

            # print(model_fit.summary())

            # Forecast for 1 year

            forecast = model_fit.forecast()[0]

            forecast = inverse_difference(X, forecast)
            print('Forecast: %f' % forecast)

            # Forecast for next 10 years

            forecast = model_fit.forecast(steps=10)[0]

            print('The Hiring rate for the next 10 years for', (i))

            history = [x for x in X]
            year = 1
            output_dataframe = self.Pred
            for yhat in forecast:
                inverted = inverse_difference(history, yhat)
                print('Year %d: %f' % (year, inverted))
                history.append(inverted)
                year += 1

            # Load back into csv
            year = 1
            entries = []
            for yhat in forecast:
                inverted = inverse_difference(history, yhat)
                if inverted < 0:
                    continue
                for j in range(0, int(abs(inverted))):
                    entries.append([str((2017+year)), 'Male', str(latlong_Coord[i])])
                    #self.Pred.append({'Entry':(2017+year), 'Gender Key':'Male', 'Coordinates':i}, ignore_index=True)
                year += 1

            location_set = pd.DataFrame(entries, columns=columns)
            output_dataframe = self.Pred.append(location_set)


        pd.DataFrame(output_dataframe).to_csv('parsed_location1_csv')



if __name__ == '__main__':
    dp = ARIMA_Coordinates()