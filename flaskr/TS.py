import itertools
from collections import OrderedDict
import pandas as pd
import googlemaps
from datetime import datetime
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming

API_key = 'AIzaSyBHD-lOFZgRIJiSSyGzA51S5jFZ6b386NU'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)

#calculate distance bwt 2 POI based on lat/long
def distance(a_position, b_position):
    now = datetime.now()
    driving = gmaps.directions(a_position, b_position, mode="driving", departure_time=now)
    
    if driving != []:
        #get driving time
        driving_time = driving[0]["legs"][0]["duration"]["text"] if driving != [] else None  #return a string
        driving_time_split = driving_time.split(" ")
        if len(driving_time_split) == 2:  # eg 34 mins or 2 hours
            time_value = driving_time_split[0]
            time_unit = driving_time_split[1]
            if time_unit  == 'min' or 'mins':
                time_value = float(time_value)/60
            if time_unit  == 'hour' or 'hours':
                time_value = float(time_value)
        if len(driving_time_split) == 4:  # eg 1 hour 4 mins
            time_value_hr = driving_time_split[0]
            time_value_min = driving_time_split[2]
            time_value = float(time_value_hr) + float(time_value_min)/60
            
         #get driving distance
        driving_distance = driving[0]["legs"][0]["distance"]["text"] if driving != [] else None  #return a string
        distance_value, distance_unit = driving_distance.split(" ")
        if distance_unit == 'mi': #eg 2,612 mi
            distance_value = float(distance_value.replace(",", ""))
        if distance_unit != 'mi': # ft or fts
            distance_value = float(distance_value.replace(",", ""))/5280  #convert to mile
             
    if driving == []:
        walking = gmaps.directions(a_position, b_position, mode="walking", departure_time=now)
        walking_time = walking[0]["legs"][0]["duration"]["text"] if walking != [] else None  #return a string
        walking_time_split = walking_time.split(" ")
        if len(walking_time_split) == 2:  # eg 34 mins or 2 hours
            time_value = walking_time_split[0]
            time_unit = walking_time_split[1]
            if time_unit  == 'min' or 'mins':
                time_value = float(time_value)/60
            if time_unit  == 'hour' or 'hours':
                time_value = float(time_value)
        if len(walking_time_split) == 4:  # eg 1 hour 4 mins
            time_value_hr = walking_time_split[0]
            time_value_min = walking_time_split[2]
            time_value = float(time_value_hr) + float(time_value_min)/60
        
        walking_distance = walking[0]["legs"][0]["distance"]["text"] if walking != [] else None  #return a string
        distance_value, distance_unit = walking_distance.split(" ")
        if distance_unit == 'mi':
            distance_value = float(distance_value.replace(",", ""))
        if distance_unit != 'mi': # ft or fts
            distance_value = float(distance_value.replace(",", ""))/5280
    
    return (time_value, distance_value)

def get_matrix(loca):
    pois = loca["thing_title"]
    n_pois = len(pois)
    geo = loca[["lat", "lon"]]
    time_matrix = np.zeros((n_pois, n_pois))
    distance_matrix = np.zeros((n_pois, n_pois))

    for i in range(distance_matrix.shape[0]):
        for j in range(distance_matrix.shape[1]):
            if j != i:
               
                a = loca["thing_title"][i]
                b = loca["thing_title"][j]
                a_position = [float(loca[loca['thing_title'] == a]['lat'].iloc[0]), float(loca[loca['thing_title'] == a]['lon'].iloc[0])]
                b_position = [float(loca[loca['thing_title'] == b]['lat'].iloc[0]), float(loca[loca['thing_title'] == b]['lon'].iloc[0])]
                time_matrix[i,j] = distance(a_position, b_position)[0]
                distance_matrix[i,j] = distance(a_position, b_position)[1]
            elif j == i:
                continue
            #else:
            #    distance_matrix[i,j] = distance_matrix[j,i]
            #    time_matrix[i,j] = time_matrix[j,i]

    return time_matrix, distance_matrix


def tsp(loca):
    start = datetime.now()
    shortest_path = None
    route_distance = shortest_time = float('inf')
    pair_time_all = {}   # save all the possible 2 POI combinations travel time
    pair_distance_all = {}   # save all the possible 2 POI combinations travel time
    pair_time_route = OrderedDict() # only save travel time of possible 2 POI combinations from shortest path
    pair_distance_route = OrderedDict() # only save travel distance of possible 2 POI combinations from shortest path
    duration = OrderedDict()
    locations = []
    
    for pair in itertools.combinations(loca['thing_title'],2):
        a_position = [float(loca[loca['thing_title'] == pair[0]]['lat']), float(loca[loca['thing_title'] == pair[0]]['lon'])]
        b_position = [float(loca[loca['thing_title'] == pair[1]]['lat']), float(loca[loca['thing_title'] == pair[1]]['lon'])]
        direction = distance(a_position, b_position)
        pair_time_all[(pair[0],pair[1])] = direction[0]
        pair_time_all[(pair[1],pair[0])] = direction[0]
        pair_distance_all[(pair[0],pair[1])] = direction[1]
        pair_distance_all[(pair[1],pair[0])] = direction[1]
    
    for path in itertools.permutations(loca['thing_title']):
        total_distance = 0
        total_time = 0
        for i in range(len(path) - 1):
            total_time += pair_time_all[(path[i],path[i+1])]
            total_distance += pair_distance_all[(path[i],path[i+1])]
        if total_time < shortest_time:
            shortest_time = total_time
            route_distance = total_distance
            shortest_path = path
      
    for i in range(len(shortest_path)-1):
        if (shortest_path[i], shortest_path[i+1]) in pair_time_all.keys():
            pair_time_route[(shortest_path[i], shortest_path[i+1])] = round(pair_time_all[(shortest_path[i], shortest_path[i+1])],1)
            pair_distance_route[(shortest_path[i], shortest_path[i+1])] = round(pair_distance_all[(shortest_path[i], shortest_path[i+1])],1)
    for i in range(len(shortest_path)):
        duration[shortest_path[i]] = float(loca[loca["thing_title"] == shortest_path[i]]["duration"])
        locations.append([float(loca[loca["thing_title"] == shortest_path[i]]["lat"]), float(loca[loca["thing_title"] == shortest_path[i]]["lon"])])
        
    locations = str(locations).replace(", ", ",")
    
    location_names = str(list(shortest_path)).replace(", ", ",").replace(" ","_").replace("'","\"")
                    
    end = datetime.now()
    cal_time = end - start
    return locations, location_names, shortest_path, round(shortest_time,1), pair_distance_route, pair_time_route, duration, cal_time


#Example1 acad park
A = {"thing_title": "Hike Double Bubble Nubble Loop with Island Explorer", "lat":44.350011499069, 'lon':-68.2414535993951, "duration": 2.0}
B = {"thing_title": "Hike Great Head Trail", "lat": 44.3300018310546, 'lon':-68.1775283813476, "duration": 4.0}
C = {"thing_title": "Hike Ship Harbor Trail", "lat": 44.2284927368164, 'lon':-68.3237609863281, "duration": 1.0}
D = {"thing_title": "Hike Giant Slide Loop", "lat": 44.35079167, 'lon':-68.30218833, "duration": 4.0}
E = {"thing_title": "Hike Gorge Path", "lat": 44.372621, 'lon':-68.221942, "duration": 3.0}
F = {"thing_title": "Hike Wonderland Trail", "lat": 44.23383331298821, 'lon':-68.3199996948242, "duration": 0.5}
G = {"thing_title": "Hike Beachcroft Path", "lat": 44.3585023529493, 'lon':-68.2059851525353, "duration": 1.5}
loca = pd.DataFrame([A,B,C,D])

locations, locations_names, shortest_path, shortest_time, pair_distance_route, pair_time_route, duration, cal_time = tsp(loca)
print("Shortest path:", shortest_path)
print("Shortest time in hour :", shortest_time)
print("Route distance in mile:", pair_distance_route)
print("Pairs time:", pair_time_route)
print("Calculation time:", cal_time)
print("duration: ", duration)
print("locations: ", locations)
print("locations names: ", locations_names)


