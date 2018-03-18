import pandas as pd
import datetime
import os
from util.utility import Utility
from pathlib import Path

ut = Utility('AttritionCSVParser')

class AttritionCSV(object):

    def __init__(self):
        self.data = {}
        self.data_workspace = str(Path(__file__).parents[2])
        self.data_workspace += os.sep + 'misc' + os.sep

        ut.context(self.data_workspace)

        df= pd.read_excel(self.data_workspace+'UNCC_Termination 2017_Rawdata.xlsx')

        self.Coulumns_of_interest = ['Personnel No.', 'Entry', 'Action type','Reason for action',
                                'Personnel Country', 'Personnel state', 'Personnel city','Chngd on','Leaving date',
                                'Cost center code','Cost Center','Gender Key','Birth date','Position','Age',
                                     'Length of Employment'];

        df.rename(columns={'Cost Ctr':'Cost center code',
                            'Job':'Position'}, inplace=True)

        print(df.head())



        df2=pd.DataFrame(df['Personnel Area'].str.split('-', 2).tolist(),
                          columns=['Personnel Country', 'Personnel state', 'Personnel city'])

        df=pd.concat([df,df2], axis=1)

        print(df.head())

        df['Birth date'] = pd.to_datetime((df['Birth date']))
        current_date_time = datetime.datetime.now()
        df['Age'] = (current_date_time - df['Birth date']).astype('<m8[Y]')
        df['Leaving date'] = pd.to_datetime(df['Leaving date'])
        df['Entry'] = pd.to_datetime(df['Entry'])
        df['Length of Employment'] = (df['Leaving date'] - df['Entry']).astype(
            '<m8[Y]')

        df.fillna('null', inplace=True)

        df = df[self.Coulumns_of_interest]

        print(df.head(2))



        df.to_csv('Cleaned_UNCC_Attrition_data1')


       # df1 = pd.read_csv(self.data_workspace+'UNCC My Success.csv',encoding='utf-8-sig')

        #df1.rename(columns={'Employee Id': 'Personnel No.',
                              #    'Cost Ctr':'Cost Center code'},inplace=True)

        #df1.drop('User Sys ID','Academic Title','Direct Reports','Functional Area','Legal Entity (Code)','Legal Entity'
               # ,'Continental Grade','Level in Organization','Total Team Size','Talent Search Consent','Goals Applicable'
                #,'Leadership Level','Career Path','(Senior) Executive Potential','Ready to move (in next 12 months)',
                #'New to Position,Expatriate,Do you have working experience in more than one Functional Area?',
                #'Comments about Functional Area,Have you worked in more than one Division level organization?',
                #'Comments about Division level,Have you worked in more than one BU level organization?',
                #'Comments about BU level,Have you worked abroad?,Comments about working abroad', axis=1)

       # print(df1.head())

        #df1.fillna('null', inplace=True)

        #df1['Date of Birth'] = pd.to_datetime(df1['Date of Birth'], errors='coerce')
        #current_date_time = datetime.datetime.now()
        #df1['Age'] = (current_date_time - df['Date of Birth']).astype('<m8[Y]')
        #df1['Leaving date'] = pd.to_datetime(df1['Leaving date'])
        #df1['Hire Date'] = pd.to_datetime(df['Hire Date'])
        #df1['Length of Employment'] = (df['Leaving date'] - df['Hire Date']).astype( '<m8[Y]')


       # print(df1.head())



         #if(df['Personnel Number'] == df1['Personnel Number']) :

        #attrition_csv = pd.merge(df, df1, on='Personnel No.', how='left')


        #attrition_csv.fillna('null', inplace=True)



    #(attrition_csv['Birth date']!= 0):





        #all_data = all_data.append(df, ignore_index=True)


        #all_data.describe()

        #print(all_data.head())

        #all_data.rename(columns={'Personnel Number':'Personnel No.',
                                   # 'Cost Ctr':'Cost Center code'},inplace=True)

        #print(all_data.head())


if __name__ == '__main__':
    dp = AttritionCSVParser()







