import yaml
import pymysql
import pandas as pd
from sqlalchemy import URL,create_engine


class ConfigClass(object):
    """Convert a dictionary to an object with attributes being the keys"""

    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])


def load_yaml(yaml_file):
    """Function for loading configuration in yaml file and make it an object to return"""
    try:
        with open(yaml_file) as f:
            config_dict = yaml.safe_load(f)
            config = ConfigClass(config_dict)
            print(f'Configuration in {yaml_file} loaded')
            return config
    except FileNotFoundError:
        print(f'ERROR - cannot find config file {yaml_file}')


def conn_to_db():
    ENDPOINT = "wanderwisely.chwnr0jplwmz.us-east-1.rds.amazonaws.com"
    PORT = 3306
    USER = "admin"
    token = "6242WW2023"
    conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT)

    url_object = URL.create(
        "mysql+pymysql",
        username=USER,
        password=token,  # plain (unescaped) text
        host=ENDPOINT,
        database="wanderwisely"
    )

    engine = create_engine(url_object)
    return conn, engine


def import_data(query, conn):
    return pd.read_sql(query, con=conn)