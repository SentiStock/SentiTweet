# Scripts to create specfic tweet related graphs

import pandas as pd


def create_tweet_sentiment_timeline(tweets, start_date, end_date):
    tweets = tweets.as_dataframe()
    # TODO create graph