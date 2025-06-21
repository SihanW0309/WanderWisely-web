import googlemaps
import pandas as pd
import math
gmaps = googlemaps.Client(key='AIzaSyBHD-lOFZgRIJiSSyGzA51S5jFZ6b386NU')

thingstodo = pd.read_csv("thingstodo.csv")

parks = pd.read_csv("activity_related_parks.csv")

parks = parks[["parkCode","parkName"]].drop_duplicates()


thingstodo["ori_lat"] = thingstodo["lat"]
thingstodo["ori_lon"] = thingstodo["lon"]
thingstodo = thingstodo.merge(parks, on = "parkCode")


nRows = len(thingstodo.index)


for i in range(nRows):

    if math.isnan(thingstodo.iloc[i,3]):
        title = thingstodo.iloc[i,1]
        parkName = thingstodo.iloc[i,-1]

        print(title, parkName)
        keyword = title+" at "+parkName

        place = gmaps.places(query=keyword)

        if len(place["results"]) == 0:
            lat = ""
            lng = ""
        else:

            lat = place["results"][0]["geometry"]["location"]["lat"]
            lng = place["results"][0]["geometry"]["location"]["lng"]

        thingstodo.iloc[i,3] = lat
        thingstodo.iloc[i,4] = lng

    else:
        continue

thingstodo.to_csv("thingstodo_update.csv")
