import pandas as pd
import datetime
import os
from util.utility import Utility
from pathlib import Path
from pygeocoder import Geocoder
from geopy.geocoders import Nominatim



class RamyaDiversityParser(object):

    def __init__(self):
        self.data = {}
        self.data_workspace = str(Path(__file__).parents[2])
        self.data_workspace += os.sep + 'misc' + os.sep



        self.diversity= pd.read_excel(self.data_workspace+'UNCC_HR Master Data active employees.xlsx')

        self.Coulumns_of_interest = ['Personnel Number', 'Entry', 'Position',
                                'Personnel Country', 'Personnel state', 'Personnel city','Employee Group','Employee Subgroup',
                                'Cost Center','Gender Key'];

        #df.rename(columns={'Cost Ctr':'Cost center code',
                            #'Job':'Position'}, inplace=True)


        df2=pd.DataFrame(self.diversity['Personnel Area'].str.split('-', 2).tolist(),
                          columns=['Personnel Country', 'Personnel state', 'Personnel city'])

        self.diversity=pd.concat([self.diversity,df2], axis=1)

        print(self.diversity.head())

        self.diversity['Entry'] = pd.to_datetime(self.diversity['Entry'])

        self.diversity = self.diversity[self.Coulumns_of_interest]

        self.diversity.dropna()

        print(self.diversity.head(2))

        print(len(self.diversity))


        #geolocator = Nominatim(self.diversity['Personnel Area','Personnel state', 'Personnel city'])
        #location = geolocator.geocode()
        #self.diversity['latitude']=location.latitude
        #self.diversity['longitude'] =location.longitude

        self.diversity.to_csv('RamyaParser')

        """for index, row in self.diversity.iterrows():

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







