import pandas as pd
import os
import numpy as np
from util.utility import Utility
from pathlib import Path
from pandas import datetime


from pandas import Series
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA
from pandas import DataFrame
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings("ignore")


# Determining p,d, q and the error rate

class Ramya_ARIMA_MSE_Coordinates(object):
    def __init__(self):
        self.data = {}
        self.data_workspace = str(Path(__file__).parents[0])
        self.data_workspace += os.sep

        self.Pred = pd.read_excel(self.data_workspace + 'RamyaCleanedDiversity.xlsx', encoding='ISO-8859-1')

        self.Years_based_columns = ['Entry', 'Gender Key', 'Latitude'];

        self.Pred = self.Pred[self.Years_based_columns]

        self.Pred['Entry'] = self.Pred['Entry'].apply(lambda x: x.strftime('%Y'))

        Gender_list = range(0, 2)



        self.df = self.Pred.groupby(['Entry', 'Gender Key']).count()  # Grouping the Gender based on the month-year

        self.df1 = self.df.unstack('Gender Key')  # Display Gender values in seperate columns

        print(self.df1.head())

        self.df1 = pd.DataFrame(self.df1, dtype='float')

        self.df1.fillna('0', inplace=True)

        self.df1.drop(self.df1.index[:23], inplace=True)


        self.df1.drop(self.df1.columns[0], axis=1, inplace=True)

        print(self.df1.head())





        X = self.df1.values
        size = int(len(X) * 0.67)
        train, test = X[0:size], X[size:len(X)]
        history = [x for x in train]
        predictions = list()
        for t in range(len(test)):
            model = ARIMA(history, order=(0, 2, 1))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
            print('predicted=%f, expected=%f' % (yhat, obs))
        error = mean_squared_error(test, predictions)
        print('Test MSE: %.3f' % error)
        # plot
        pyplot.plot(test)
        pyplot.plot(predictions, color='red')
        pyplot.show()



        # evaluate an ARIMA model for a given order (p,d,q)
        def evaluate_arima_model(X, arima_order):
            # prepare training dataset
            train_size = int(len(X) * 0.66)
            train, test = X[0:train_size], X[train_size:]
            history = [x for x in train]
            # make predictions
            predictions = list()
            for t in range(len(test)):
                model = ARIMA(history, order=arima_order)
                model_fit = model.fit(disp=0)
                yhat = model_fit.forecast()[0]
                predictions.append(yhat)
                history.append(test[t])
            # calculate out of sample error
            error = mean_squared_error(test, predictions)
            return error




        # evaluate an ARIMA model for a given order (p,d,q)
        def evaluate_arima_model(X, arima_order):
            # prepare training dataset
            train_size = int(len(X) * 0.66)
            train, test = X[0:train_size], X[train_size:]
            history = [x for x in train]
            # make predictions
            predictions = list()
            for t in range(len(test)):
                model = ARIMA(history, order=arima_order)
                model_fit = model.fit(disp=0)
                yhat = model_fit.forecast()[0]
                predictions.append(yhat)
                history.append(test[t])
            # calculate out of sample error
            error = mean_squared_error(test, predictions)
            return error

        def evaluate_models(dataset, p_values, d_values, q_values):
            dataset = dataset.astype('float32')
            best_score, best_cfg = float("inf"), None
            for p in p_values:
                for d in d_values:
                    for q in q_values:
                        order = (p, d, q)
                        try:
                            mse = evaluate_arima_model(dataset, order)
                            if mse < best_score:
                                best_score, best_cfg = mse, order
                            print('ARIMA%s MSE=%.3f' % (order, mse))
                        except:
                            continue
            print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))

        # evaluate parameters
        p_values = [0, 1, 2, 4, 6, 8, 10]
        d_values = range(0, 3)
        q_values = range(0, 3)
        warnings.filterwarnings("ignore")
        evaluate_models(self.df1.values, p_values, d_values, q_values)




if __name__ == '__main__':
    dp = Ramya_ARIMA_MSE_Coordinates()