import os
import tweepy
import pandas as pd

from tweet.models import HashTag, Tweet


consumer_key = os.getenv('TWITTER_KEY')
consumer_secret = os.getenv('TWITTER_SECRET_SECRET_KEY')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
twitter_api = tweepy.API(auth)

twitter_client = tweepy.Client(
    bearer_token=None,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
) # TODO setup client, which is 2.0


def get_sentiment(tweets):
    # TODO get tweet sentiment
    pass

def get_and_create_hashtags(tweets):
    for tweet in tweets:
        hashtags = [j for j in [i for i in tweet.text.split() if i.startswith('#')]]
        for hashtag in hashtags:
            tag, created = HashTag.objects.get_or_create(value=hashtag)
            tag.tweets.add(tweet)
            [tag.companies.add(i) for i in tweet.companies]
            tag.save()


def clean_tweets(tweets):
    # TODO this is old code

    if isinstance(tweets, Tweet):
        df = tweets.as_dataframe()
    else:
        df = tweets

    df.drop_duplicates(subset=["id"],inplace=True)

    new_tweets = []

    for index, tweet in df.iterrows():
        stop_words = self.__get_stopwords(lang)
        stemmer = self.__get_stemmer(lang)
        tweet.cleaned_text = self.__clean_text(tweet.text, stop_words, stemmer)
        new_tweets.append(list(tweet))

    cleaned_df = pd.DataFrame(new_tweets, columns=[col for col in df])

    # Remove empty reviews
    cleaned_df = cleaned_df.loc[lambda x: x['text'] != '']

    # Drop duplicates after cleaning
    cleaned_df.drop_duplicates(subset=["text"],inplace=True)
    cleaned_df.reset_index(inplace=True, drop=True)

    return cleaned_df

    def __clean_text(self, text, stop_words, stemmer):
        whitelist = set('abcdefghijklmnopqrstuvwxyz# ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        clean_text = text.replace("<br>", " ")
        clean_text = clean_text.replace("\n", " ")
        clean_text = clean_text.encode('ascii', 'ignore').decode('ascii')
        clean_text = ''.join(i + ' ' for i in clean_text.split() if not i.startswith('http') and not i.startswith('@'))
        clean_text = ''.join(i + ' ' for i in [stemmer.stem(word) for word in clean_text.lower().split() if word not in stop_words])
        return ''.join(filter(whitelist.__contains__, clean_text))

    def __get_stopwords(self, language):
        """
        Cobine nltk's and hotel reviews specific stopwords and returns these as a set
        """
        stop_words = stopwords.words(language)
        return list(set(stop_words))

    def __get_stemmer(self, language):
        stemmer = nltk.stem.SnowballStemmer(language, ignore_stopwords=True)
        return stemmer


def get_tweets_by_hashtag(hashtag):
    # TODO transfer to 2.0
    MAX_TWEETS = 3000
    tweets = tweepy.Cursor(
        twitter_api.search_tweets,
        q=f'{hashtag} -filter:retweets',
        tweet_mode='extended'
    ).items(MAX_TWEETS)

    print(vars(tweets))

    tweets_data = [[
        tweet.id,
        tweet.full_text,
        tweet.lang,
        tweet.created_at,
        tweet.user.id,
        tweet.user.location,
    ] for tweet in tweets]

    df = pd.DataFrame(data=tweets_data, columns=[
        'id',
        'text',
        'language',
        'post_date',
        'user_id',
        'user_location',
        'geo_location'
    ])

    df.rename(columns={'ticker_symbol':'company_id'}, inplace=True)

    return df

def get_tweets_for_company(company):
    hashtags = company.hashtags.all()
    for hashtag in hashtags:
        get_tweets_by_hashtag(hashtag)
