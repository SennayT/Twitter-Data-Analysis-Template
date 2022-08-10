import pandas as pd
import re
import string

class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[(df != df.columns).all(axis=1)].index
        df.drop(unwanted_rows , inplace=True)
        
        return df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        df.drop_duplicates(subset=['original_text'],inplace=True)
        return df

    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        df['created_at'] = pd.to_datetime(df['created_at'])
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df['polarity'] = pd.to_numeric(df['polarity'])
        df['subjectivity'] = pd.to_numeric(df['subjectivity'])
        df['retweet_count'] = pd.to_numeric(df['retweet_count'])
        df['favorite_count'] = pd.to_numeric(df['favorite_count'])
        df['followers_count'] = pd.to_numeric(df['followers_count'])
        df['friends_count'] = pd.to_numeric(df['friends_count'])
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        unwanted_rows = df[df['lang'] != 'en'].index
        df.drop(unwanted_rows , inplace=True)

        
        return df

    def clean_text(txt):
        txt = re.sub(r"RT[\s]+", "", txt)
        txt = txt.replace("\n", " ")
        txt = re.sub(" +", " ", txt)
        txt = re.sub(r"https?:\/\/\S+", "", txt)
        txt = re.sub(r"(@[A-Za-z0–9_]+)|[^\w\s]|#", "", txt)
        # txt = emoji.replace_emoji(txt, replace='')
        txt.strip()
        return txt

    def clean_tweet_original_text(self, df: pd.DataFrame) -> pd.DataFrame:
        df["clean_text"] = df["original_text"].apply(self.clean_text)
        df['clean_text'] = df['clean_text'].astype(str)
        df['clean_text'] = df['clean_text'].apply(lambda x: x.lower())
        df['clean_text'] = df['clean_text'].apply(lambda x: x.translate(str.maketrans(' ', ' ', string.punctuation)))
        return df
