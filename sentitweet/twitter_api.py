import os
import tweepy
import pandas as pd

from sentitweet.utils import create_from_df

from tweet.models import Tweet, TwitterUser
from tweet.utils import get_and_create_hashtags


bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
Client = tweepy.Client(bearer_token)#, return_type=dict)


def get_tweets_by_hashtag(hashtag, MAX_TWEETS=10):
    tweets = Client.search_recent_tweets(
        query=f'{hashtag} new -is:retweet', 
        expansions=['author_id', 'geo.place_id'],
        tweet_fields=['created_at', 'lang', 'author_id', 'public_metrics', 'source'], # TODO context_annotations # TODO A lot of info!!!
        user_fields=['created_at', 'username', 'name'],
        since_id=None,
        max_results=MAX_TWEETS,
    )

    users_data = [[
        user.id,
        user.name,
        user.username,
        user.created_at,
    ] for user in tweets.includes['users']]

    tweets_data = [[
        tweet.id,
        tweet.text,
        tweet.lang,
        tweet.created_at,
        tweet.public_metrics['reply_count'],
        tweet.public_metrics['retweet_count'],
        tweet.public_metrics['like_count'],
    ] for tweet in tweets.data]

    tweets_df = pd.DataFrame(data=tweets_data, columns=[
        'id',
        'text',
        'language',
        'post_date',
        'comment_number',
        'retweet_number',
        'like_number'
    ])

    users_df = pd.DataFrame(data=users_data, columns=[
        'id',
        'name',
        'username',
        'created_at',
    ])

    tweets_df.drop_duplicates(subset=['id'], inplace=True)
    users_df.drop_duplicates(subset=['id'], inplace=True)

    return tweets_df, users_df

def get_tweets_for_company(company):
    hashtags = company.get_top_hashtags()

    for hashtag in hashtags:
        tweets_df, users_df = get_tweets_by_hashtag(hashtag)
        company_tweets_df = pd.DataFrame({'tweet_id': tweets_df['id'], 'company_id': company.id})

        # TODO no way of checking if the id/text already exists 
        # TODO We can upload one by one --> should argue what is best
        create_from_df(TwitterUser, users_df)
        create_from_df(Tweet, tweets_df)
        create_from_df(None, company_tweets_df, table='tweet_tweet_companies')

        new_tweets = Tweets.objects.filter(id__in=list(tweets_df['id']))
        get_and_create_hashtags(new_tweets)
