import os
import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
from extract_dataframe import read_json
from extract_dataframe import TweetDfExtractor
from clean_tweets_dataframe import Clean_Tweets


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


def create_tables():
    conn, cur = db_connect()
    sql_file = 'day5_schema.sql'
    fd = open(sql_file, 'r')
    read_sql_file = fd.read()
    fd.close()

    commands = read_sql_file.split(';')
    for command in commands:
        try:
            res = cur.execute(command)
        except Error as ex:
            print("Command skipped: ", command)
            print(ex)
    conn.commit()
    conn.close()
    return


def get_df() -> pd.DataFrame:
    _, tweet_list = read_json("data/global_twitter_data.json")
    tweets = TweetDfExtractor(tweet_list)
    df = tweets.get_tweet_df()
    return df


def pre_process(df: pd.DataFrame) -> pd.DataFrame:
    cl = Clean_Tweets(df)
    df = cl.clean_tweet_original_text(df)
    df = cl.convert_to_datetime(df)
    df = cl.remove_non_english_tweets(df)
    df = cl.convert_to_numbers(df)
    return df
