import pandas as pd
import datetime



df=pd.read_csv("C:/Users/divya1/ContinentalPredictiveAnalytics/misc/UNCC_Termination 2017_Rawdata_1.csv")
#print(df.head())

df = df.astype(object).where(pd.notnull(df),None)


df['Birth date']= pd.to_datetime((df['Birth date']))
current_date_time = datetime.datetime.now()
df['Age'] = (current_date_time - df['Birth date']).astype('<m8[Y]')
df['Leaving date'] = pd.to_datetime(df['Leaving date'])
df['Entry'] = pd.to_datetime(df['Entry'])
df['Length of Employment'] = (df['Leaving date'] - df['Entry']).astype('<m8[Y]')
#df.columns

df.to_csv('Cleaned_UNCC_Attritiondata1')






