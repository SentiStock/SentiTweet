import os

import nltk
import pandas as pd
from nltk.corpus import stopwords
from tweet.models import HashTag, Tweet


def get_sentiment(tweets):
    # TODO get tweet sentiment
    pass

def get_and_create_hashtags(tweets):
    for tweet in tweets:
        hashtags = [j for j in [i for i in tweet.text.split() if i.startswith('#')]]
        for hashtag in hashtags:
            tag, created = HashTag.objects.get_or_create(value=hashtag)
            tag.tweets.add(tweet)
            [tag.companies.add(i) for i in tweet.companies.all()]
            tag.save()


def clean_tweet_text(text):
    stemmer = nltk.stem.SnowballStemmer('english', ignore_stopwords=True)
    stop_words = list(set(stopwords.words('english')))
    whitelist = set('abcdefghijklmnopqrstuvwxyz# ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    clean_text = text.replace("<br>", " ")
    clean_text = clean_text.replace("\n", " ")
    clean_text = clean_text.encode('ascii', 'ignore').decode('ascii')
    clean_text = ''.join(i + ' ' for i in clean_text.split() if not i.startswith('http') and not i.startswith('@'))
    clean_text = ''.join(i + ' ' for i in [stemmer.stem(word) for word in clean_text.lower().split() if word not in stop_words])
    return ''.join(filter(whitelist.__contains__, clean_text))


def clean_tweets(tweets):
    for tweet in tweets:
        tweet.cleaned_text = clean_tweet_text(tweet.text)
        tweet.save()
