import helper_functions as uf

import requests
import json
from flatten_json import flatten
import pandas as pd

from constants import auth_config_path, data_config_path, data_wd


class NPSdataRetriever:
    """class for retrieve data through NPS API

    """

    def __init__(self, authentication: dict, data_config: object):
        """initialize object with API authentication and data configuration

        :param authentication: dict of api authorization, e.g. {'api_key': 'xxxxxx'}
        :param data_config: data configuration object
        """
        self.auth = authentication
        self.data_config = data_config
        self.api_config = uf.ConfigClass(data_config.API)
        self.filename_config = uf.ConfigClass(data_config.filename)

    def get_activities(self):
        """function for retrieving activities possible in national parks

        :return: dataframe including activity id and name
        """
        url = self.api_config.get_activities_url
        r = requests.get(url, params=self.auth)
        data = pd.DataFrame(json.loads(r.text)['data'])
        print(data.shape)
        print(data.head())
        filepath = data_wd + self.filename_config.activities
        data.to_csv(filepath, index=False)
        print(f"Activity data were retrieved and saved in {filepath}")
        return data

    def get_activity_related_parks(self):
        """function for retrieving national parks related to specific activities

        :return:
        """
        url = self.api_config.get_activity_related_park_url
        r = requests.get(url, params=self.auth)
        raw_data = json.loads(r.text)['data']
        data_list = []
        for activity in raw_data:
            for park in activity['parks']:
                data_dict = {'id'         : activity['id'],
                             'name'       : activity['name'],
                             'designation': park['designation'],
                             'state'      : park['states'],
                             'parkCode'   : park['parkCode'],
                             'parkName'   : park['fullName']
                             }
                data_list.append(data_dict)
        data = pd.DataFrame(data_list)
        national_park_data = data[data['designation'] == 'National Park'].copy()
        print(national_park_data.shape)
        print(national_park_data.head())
        filepath = data_wd + self.filename_config.activity_related_parks
        national_park_data.to_csv(filepath, index=False)
        print(f"Activity-related park data were retrieved and saved in {filepath}")
        return data

    def get_amenities(self):
        """function for retrieving amenities in national parks

        :return: dataframe including amenities id and name
        """
        url = self.api_config.get_amenities_url
        r = requests.get(url, params=self.auth)
        response = json.loads(r.text)
        if int(response['total']) > int(response['limit']):
                print(f"The number of response ({int(response['total'])}) exceeds the default limit 50")
                params = self.auth
                params['limit'] = int(response['total'])
                r = requests.get(url, params=params)
        data = pd.DataFrame(json.loads(r.text)['data']).drop(columns=['categories'])
        print(data.shape)
        print(data.head())
        filepath = data_wd + self.filename_config.amenities
        data.to_csv(filepath, index=False)
        print(f"Amenity data were retrieved and saved in {filepath}")
        return data

    def get_amenity_related_parks(self):
        """function for retrieving national parks related to specific amenities

        :return:
        """
        url = self.api_config.get_amenity_related_park_url
        r = requests.get(url, params=self.auth)
        raw_data = json.loads(r.text)['data']
        data_list = []
        for amenity in raw_data:
            for park in amenity[0]['parks']:
                data_dict = {'id'         : amenity[0]['id'],
                             'name'       : amenity[0]['name'],
                             'designation': park['designation'],
                             'state'      : park['states'],
                             'parkCode'   : park['parkCode'],
                             'parkName'   : park['fullName']
                             }
                data_list.append(data_dict)
        data = pd.DataFrame(data_list)
        national_park_data = data[data['designation'] == 'National Park'].copy()
        print(national_park_data.shape)
        print(national_park_data.head())
        filepath = data_wd + self.filename_config.amenity_related_parks
        national_park_data.to_csv(filepath, index=False)
        print(f"Amenity-related park data were retrieved and saved in {filepath}")
        return data
        

    def get_campground(self):
        """

        :return:
        """
        url = self.api_config.get_campground_url
        park = pd.read_csv(data_wd + self.filename_config.activity_related_parks)
        parkcode = park['parkCode'].unique().tolist()
        data_list = []
        for code in parkcode:
            params = self.auth
            params['parkCode'] = code
            params['limit'] = 50
            r = requests.get(url, params=params)
            response = json.loads(r.text)
            if int(response['total']) > int(response['limit']):
                print(f"The number of response ({int(response['total'])}) exceeds the default limit 50")
                params.update({'limit': int(response['total'])})
                r = requests.get(url, params=params)
            raw_data = json.loads(r.text)['data']
            for campground in raw_data:
                data_dict = {'id':              campground['id'],
                             'name':            campground['name'],
                             'parkCode':        code,
                             'lat':             campground['latitude'],
                             'lon':             campground['longitude'],
                             'campground_url':  campground['url'],
                             'reservation_url': campground['reservationUrl'],
                             'info':            campground['description']
                             }
                if len(campground['addresses']) > 0:
                    add = campground['addresses'][0]
                    data_dict['address'] = add['line1'] + ' ' \
                                           + add['line2'] + ' ' \
                                           + add['line3'] + ' ' \
                                           + add['city'] + ' ' \
                                           + add['stateCode'] + ' ' \
                                           + add['postalCode']
                else:
                    data_dict['address'] = ''
                data_list.append(data_dict)
        data = pd.DataFrame(data_list)
        print(data.shape)
        print(data.head())
        filepath = data_wd + self.filename_config.campground
        data.to_csv(filepath, index=False)
        print(f"Park-related place data were retrieved and saved in {filepath}")
        return data

    def get_places(self):
        """

        :return:
        """
        url = self.api_config.get_places_url
        park = pd.read_csv(data_wd + self.filename_config.activity_related_parks)
        parkcode = park['parkCode'].unique().tolist()
        data_list = []
        for code in parkcode:
            params = self.auth
            params['parkCode'] = code
            params['limit'] = 50
            r = requests.get(url, params=params)
            response = json.loads(r.text)
            if int(response['total']) > int(response['limit']):
                print(f"The number of response ({int(response['total'])}) exceeds the default limit 50")
                params.update({'limit': int(response['total'])})
                r = requests.get(url, params=params)
            raw_data = json.loads(r.text)['data']
            for place in raw_data:
                if place['isOpenToPublic'] == '1':
                    data_dict = {'id'         : place['id'],
                                 'place_title': place['title'],
                                 'parkCode'   : code,
                                 'lat'        : place['latitude'],
                                 'lon'        : place['longitude'],
                                 'place_url'  : place['url'],
                                 'image_url'  : place['images'][0]['url'],
                                 'tags'       : place['tags'],
                                 'info'       : place['listingDescription']
                                 }
                    data_list.append(data_dict)
                else:
                    continue
        data = pd.DataFrame(data_list)
        print(data.shape)
        print(data.head())
        filepath = data_wd + self.filename_config.park_related_places
        data.to_csv(filepath, index=False)
        print(f"Park-related place data were retrieved and saved in {filepath}")
        return data

    def get_thingstodo(self):
        """

        :return:
        """
        url = self.api_config.get_thingstodo_url
        park = pd.read_csv(data_wd + self.filename_config.activity_related_parks)
        parkcode = park['parkCode'].unique().tolist()
        data_list = []
        for code in parkcode:
            params = self.auth
            params['parkCode'] = code
            params['limit'] = 50
            r = requests.get(url, params=params)
            response = json.loads(r.text)
            if int(response['total']) > int(response['limit']):
                print(f"The number of response ({int(response['total'])}) exceeds the default limit 50")
                params.update({'limit': int(response['total'])})
                r = requests.get(url, params=params)
            raw_data = json.loads(r.text)['data']
            for thing in raw_data:
                    data_dict = {'id'         : thing['id'],
                                 'thing_title': thing['title'],
                                 'parkCode'   : code,
                                 'lat'        : thing['latitude'],
                                 'lon'        : thing['longitude'],
                                 'locaton'    : thing['location'],
                                 'place_url'  : thing['url'],
                                 'image_url'  : thing['images'][0]['url'],
                                 'durtion'    : thing['duration'],
                                 'tags'       : thing['tags'],
                                 'info'       : thing['shortDescription'],
                                 'activity_id': thing['activities'][0]['id'],
                                 'activity_name': thing['activities'][0]['name']
                                 }
                    data_list.append(data_dict)
        data = pd.DataFrame(data_list)
        print(data.shape)
        print(data.head())
        filepath = data_wd + self.filename_config.thingstodo
        data.to_csv(filepath, index=False)
        print(f"Things-to-do were retrieved and saved in {filepath}")
        return data


if __name__ == '__main__':
    auth = uf.load_yaml(auth_config_path).NPS
    nps_data_config = uf.ConfigClass(uf.load_yaml(data_config_path).NPS)
    nps_data_retriever = NPSdataRetriever(auth, nps_data_config)
    data = nps_data_retriever.get_places()

