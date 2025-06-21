import pymysql
import sys
import boto3
import os
import pandas as pd
from sqlalchemy import URL,create_engine

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

def sql_query(query, conn):
    return pd.read_sql(query, con=conn)





if __name__ == "__main__":
    # load data
    tables = []
    files = os.listdir("data sample/")
    for f in files:
        if f.endswith(".csv"):
            tables.append(pd.read_csv("data sample/" + f))

    # create database
    # sql = '''create database wanderwisely'''
    # conn.cursor().execute(sql)
    # conn.commit()

    # build connection and engine
    conn, engine = conn_to_db()

    # create tables
    # tables[0].to_sql("activity_related_parks", con = engine, if_exists="replace")
    # tables[1].to_sql("park_related_places", con = engine, if_exists="replace")
    # tables[2].to_sql("amenity_related_parks", con = engine, if_exists="replace")


    arp = sql_query("select * from wanderwisely.amenity_related_parks", conn)