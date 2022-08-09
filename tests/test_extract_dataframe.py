import unittest
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join("../")))

from extract_dataframe import read_json
from extract_dataframe import TweetDfExtractor

# For unit testing the data reading and processing codes, 
# we will need about 5 tweet samples. 
# Create a sample not more than 10 tweets and place it in a json file.
# Provide the path to the samples tweets file you created below
sampletweetsjsonfile = "sampletweets.json"   #put here the path to where you placed the file e.g. ./sampletweets.json.
_, tweet_list = read_json(sampletweetsjsonfile)

columns = [
    "created_at",
    "source",
    "original_text",
    "clean_text",
    "sentiment",
    "polarity",
    "subjectivity",
    "lang",
    "favorite_count",
    "retweet_count",
    "original_author",
    "screen_count",
    "followers_count",
    "friends_count",
    "possibly_sensitive",
    "hashtags",
    "user_mentions",
    "place",
    "place_coord_boundaries",
]


class TestTweetDfExtractor(unittest.TestCase):
    """
		A class for unit-testing function in the fix_clean_tweets_dataframe.py file

		Args:
        -----
			unittest.TestCase this allows the new class to inherit
			from the unittest module
	"""

    def setUp(self) -> pd.DataFrame:
        self.df = TweetDfExtractor(tweet_list[:5])
        # tweet_df = self.df.get_tweet_df()

    def test_find_statuses_count(self):
        self.assertEqual(
            self.df.find_statuses_count(), [888, 1597, 2293, 44, 1313]
        )

    def test_find_full_text(self):
        text = ['#Pelosi airplane landed safely in #Taiwan 🇹🇼  \n1) - Both 🇨🇳 &amp;  🇺🇸 are playing "win win" on financial markets. 2) - Taiwan may be the future Asian   Cuba  3) - 🇺🇸 &amp; 🇨🇳 need an Asian #NATO / #5G\nWhat\'s your thoughts?',
                'Watch the video of the beginning of the Chinese bombing of Taiwan during Pelosi visit from here : https://t.co/twah6WU4fZ\nــــــــــــــــــــــــــ\n#Pelosi #マツコの知らない世界 #Yediiklim #BadDecisionsTrailer1 #LawnBowls #祝_CALL119_MV900万回 #มากอดกันนะซีพฤกษ์ https://t.co/m4CXfyZRS7',
                '#Pelosi \n#Taipei \n#taiwan\n#XiJinping \n#China \nOn a verge of another war https://t.co/DuqDiSnWcd',
                '#HOBIPALOOZA #LaAcademiaExpulsion #WEURO2022 #jhopeAtLollapalooza #SuzukiPakistan #Fantastico #Taiwan #breastfeeding #Kosovo #BORNPINK  strong ✍️💜 https://t.co/GtZeNL24rm',
                '#Pelosi\n#china\nChina Time ✌️ https://t.co/tEDjzTlszu']

        self.assertEqual(self.df.find_full_text(), text)

    def test_find_sentiments(self):
        self.assertEqual(
            self.df.find_sentiments(self.df.find_full_text()),
            (
                [0.3, 0.0, 0.0, 0.4333333333333333, 0.0],
                [0.20357142857142857, 0.0, 0.0, 0.7333333333333333, 0.0]
            ),
        )


    def test_find_screen_name(self):
        names = ['DzCritical', 'toopsat', 'NassimaLilEmy', 'd_dhayae', 'Mohamme65404115']
        self.assertEqual(self.df.find_screen_name(), names)

    def test_find_followers_count(self):
        f_count = [318, 764, 64, 60, 39]
        self.assertEqual(self.df.find_followers_count(), f_count)

    def test_find_friends_count(self):
        friends_count = [373, 144, 47, 463, 206]
        self.assertEqual(self.df.find_friends_count(), friends_count)

    def test_find_is_sensitive(self):
        self.assertEqual(self.df.is_sensitive(), [False, False, False, False, False])


    def test_find_hashtags(self):
        hashtags = [
            # item 1
            [{'text': 'Pelosi', 'indices': [0, 7]},
             {'text': 'Taiwan', 'indices': [34, 41]},
             {'text': 'NATO', 'indices': [189, 194]},
             {'text': '5G', 'indices': [197, 200]}],
            # item 2
            [{'text': 'Pelosi', 'indices': [149, 156]},
             {'text': 'マツコの知らない世界', 'indices': [157, 168]},
             {'text': 'Yediiklim', 'indices': [169, 179]},
             {'text': 'BadDecisionsTrailer1', 'indices': [180, 201]},
             {'text': 'LawnBowls', 'indices': [202, 212]},
             {'text': '祝_CALL119_MV900万回', 'indices': [213, 231]},
             {'text': 'มากอดกันนะซีพฤกษ์', 'indices': [232, 250]}],
            # item 3
            [{'text': 'Pelosi', 'indices': [0, 7]},
             {'text': 'Taipei', 'indices': [9, 16]},
             {'text': 'taiwan', 'indices': [18, 25]},
             {'text': 'XiJinping', 'indices': [26, 36]},
             {'text': 'China', 'indices': [38, 44]}],
            [{'text': 'HOBIPALOOZA', 'indices': [0, 12]},
             # item 4
             {'text': 'LaAcademiaExpulsion', 'indices': [13, 33]},
             {'text': 'WEURO2022', 'indices': [34, 44]},
             {'text': 'jhopeAtLollapalooza', 'indices': [45, 65]},
             {'text': 'SuzukiPakistan', 'indices': [66, 81]},
             {'text': 'Fantastico', 'indices': [82, 93]},
             {'text': 'Taiwan', 'indices': [94, 101]},
             {'text': 'breastfeeding', 'indices': [102, 116]},
             {'text': 'Kosovo', 'indices': [117, 124]},
             {'text': 'BORNPINK', 'indices': [125, 134]}],
            # item 5
            [{'text': 'Pelosi', 'indices': [0, 7]},
             {'text': 'china', 'indices': [8, 14]}]]
        self.assertEqual(self.df.find_hashtags(), hashtags)

    def test_find_mentions(self):
        mentions = [[], [], [], [], []]
        self.assertEqual(self.df.find_mentions(), mentions)



if __name__ == "__main__":
    unittest.main()

