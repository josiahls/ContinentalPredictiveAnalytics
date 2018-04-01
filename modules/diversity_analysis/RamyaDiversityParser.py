import pandas as pd
import datetime
import os
from util.utility import Utility
from pathlib import Path
from pygeocoder import Geocoder
import requests
from geopy.geocoders import Nominatim



class RamyaDiversityParser(object):

    def __init__(self):
        self.data = {}
        self.data_workspace = str(Path(__file__).parents[2])
        self.data_workspace += os.sep + 'misc' + os.sep



        self.diversity= pd.read_excel(self.data_workspace+'UNCC_HR Master Data active employees.xlsx')

        self.Coulumns_of_interest = ['Personnel Number', 'Entry', 'Job Title',
                                'Personnel Country', 'Personnel state', 'Personnel city','Employee Group','Employee Subgroup',
                                'Cost Center','Gender Key'];

        #df.rename(columns={'Cost Ctr':'Cost center code',
                            #'Job':'Position'}, inplace=True)hg




        df2=pd.DataFrame(self.diversity['Personnel Area'].str.split('-', 2).tolist(),
                          columns=['Personnel Country', 'Personnel state', 'Personnel city'])

        self.diversity=pd.concat([self.diversity,df2], axis=1)



        self.diversity['Entry'] = pd.to_datetime(self.diversity['Entry'])

        self.diversity = self.diversity[self.Coulumns_of_interest]

        print(self.diversity.head(3))




        self.diversity.to_csv('RamyaParser1')

        #self.diversity_coordinates = pd.read_excel(self.data_workspace + 'RamyaCleanedDiversity.xlsx', encoding = 'ISO-8859-1')

        #print(self.diversity_coordinates.head(3))



        """self.diversity['Location'] = str (self.diversity['Personnel city']+',' + self.diversity['Personnel state']+',' + self.diversity['Personnel Country'])

        geolocator = Nominatim()

        self.diversity['result'] = geolocator.geocode(self.diversity['Personnel state'])

        self.diversity = self.diversity[self.Coulumns_of_interest]

        #self.diversity['Personnel state'].drop('All', inplace=True)





        print(self.diversity.head(2))

        print(len(self.diversity))


        #geolocator = Nominatim(self.diversity['Personnel Area','Personnel state', 'Personnel city'])
        #location = geolocator.geocode()
        #self.diversity['latitude']=location.latitude
        #self.diversity['longitude'] =location.longitude



        #self.diversity=[self.diversity['Personnel state'] != 'All']

        #geolocator=Nominatim()
        #self.diversity['city_coord'] = self.diversity['Personnel state'].apply(geolocator.geocode)
        #self.diversity['city_coord'] = self.diversity['city_coord'].apply(lambda x: (x.latitude, x.longitude))

        #states = self.diversity['Personnel state'].unique()

        #print(states)
        #d = dict(zip(states, pd.Series(states).apply(geolocator.geocode).apply(lambda x: (x.latitude, x.longitude))))
        #self.diversity['city_coord'] = self.diversity['Personnel state'].map(d)



        print(self.diversity.head(10))

         self.diversity.to_csv('RamyaParser')

         for index, row in self.diversity.iterrows():

         self.diversity['location'] = str(row['Personnel city'] + ', ' + row['Personnel state']+ ', ' + row['Personnel Area'])

         print(self.diversity.head())

         result = Geocoder.geocode(location)
         coords = str(result[0].coordinates)

         chars_to_remove = ['(', ')']
         coords = coords.translate(None, ''.join(chars_to_remove))

         lat = float(coords.split(',')[0])
         long = float(coords.split(',')[1])

         line = pd.Series([city, nation, lat, long])"""

        #info = info.append(line, ignore_index=Trdiversity.to_csv('RamyaParser')ue)


        #



if __name__ == '__main__':
    dp = RamyaDiversityParser()







