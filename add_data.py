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

    drop = ['possibly_sensitive', 'original_text', 'user_mentions', 'hashtags']
    try:
        df = df.drop(drop, axis=1)
        df = df.fillna(0)
    except KeyError as e:
        print('key error', e)

    return df


def insert_tweet_to_table():
    conn, cur = db_connect()
    df = get_df()
    df = pre_process(df)
    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO TweetInformation (created_at, source, polarity, subjectivity, lang,
                        favorite_count, retweet_count, screen_name, original_author, followers_count, friends_count
                        , place, clean_text)
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                row[12])

        try:
            # Execute the SQL command
            cur.execute(sqlQuery, data)
            # Commit your changes in the database
            conn.commit()
        except Error as e:
            conn.rollback()
            print("Error: ", e.args)
    print('data inserted')


insert_tweet_to_table()
