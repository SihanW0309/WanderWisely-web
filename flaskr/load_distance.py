import pandas as pd
import googlemaps
from itertools import tee

df = pd.read_csv(data_wd + self.filename_config.activity_related_parks,usecols = ['id','lat','lon'])


API_key = ''#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


list = [0]
   
for (i1, row1), (i2, row2) in pairwise(df.iterrows()):
          #origin points
          LatOrigin = row1['lat'] 
          LongOrigin = row1['lon']
          origins = (LatOrigin,LongOrigin)

          #destination point
          LatDest = row2['lat']   # Save value as lat
          LongDest = row2['lon'] # Save value as lat
          destination = (LatDest,LongDest)

          result = gmaps.distance_matrix(origins, destination, mode='walking')["rows"][0]["elements"][0]['distance']["value"]
          list.append(result)
          
df['Distance'] = list
filepath = data_wd + self.filename_config.distances
data.to_csv(filepath, index=False)
print(f"Park-related place data were retrieved and saved in {filepath}")
return data
      

