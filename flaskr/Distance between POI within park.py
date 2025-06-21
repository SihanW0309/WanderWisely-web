import pandas as pd
import googlemaps
from collections import defaultdict
from datetime import datetime


# load park and point of interest data
df = pd.read_csv('park_related_places.csv')

# load google map API
API_key = 'AIzaSyBHD-lOFZgRIJiSSyGzA51S5jFZ6b386NU'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)

#get unique park code
parks = df["parkCode"].unique()

# loop through parks
distance = defaultdict(dict)
for park in parks[0:1]:
    is_park = df["parkCode"] == park
    pois = df[is_park][["id","placeID", "lat", "lon"]]

    # loop through point of interest and calculate distance
    for ind_a, row_a in pois.iterrows():
        a_position = (row_a["lat"],row_a["lon"])
        for ind_b, row_b in pois.iterrows():
                now = datetime.now()
                if row_b["id"] == row_a["id"]:
                    continue

                b_position = (row_b["lat"], row_b["lon"])

                # calculate distance
                walking = gmaps.directions(a_position,b_position,mode = "walking",departure_time = now)
                walking_time = walking[0]["legs"][0]["duration"]["text"] if walking !=[] else None
                walking_distance =  walking[0]["legs"][0]["distance"]["text"] if walking !=[] else None

                driving = gmaps.directions(a_position, b_position, mode="driving", departure_time=now)
                driving_time = driving[0]["legs"][0]["duration"]["text"] if driving != [] else None
                driving_distance = driving[0]["legs"][0]["distance"]["text"] if driving != [] else None

                # compile distance dict
                distance_key = park+":"+ row_a["id"]+ ":"+ row_b["id"]
                distance_value = {"walking_distance": walking_distance,
                                  "walking_time": walking_time,
                                  "driving_distance": driving_distance,
                                  "driving_time": driving_time
                                  }

                distance[distance_key] = distance_value

distance_df = pd.DataFrame.from_dict(distance,orient="index")
distance_df.reset_index(inplace=True)
distance_df[["parkCode", "id_1", "id_2"]] = distance_df["index"].str.split(":", expand=True)
distance_df.drop(["index"], axis = 1, inplace=True)







