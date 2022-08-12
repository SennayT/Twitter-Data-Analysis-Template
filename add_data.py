import os
import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
from extract_dataframe import read_json
from extract_dataframe import TweetDfExtractor


def db_connect():
    conn = mysql.connect(
        host='localhost',
        user='sennay',
        password='secret',
        database='twitter',
        buffered=True
    )
    cur = conn.cursor()
    return conn, cur
