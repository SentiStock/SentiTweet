import os

import pandas as pd
import tweepy
from django.db.models import Count
from tweet.models import Tweet, TwitterUser
from tweet.utils import get_and_create_hashtags

from sentitweet.utils import create_from_df

bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
Client = tweepy.Client(bearer_token)#, return_type=dict)


def process_api_response(response):
    users_data = [[
        user.id,
        user.name,
        user.username,
        user.created_at,
    ] for user in response.includes['users']]

    tweets_data = [[
        tweet.id,
        tweet.text,
        tweet.lang,
        tweet.created_at,
        tweet.author_id,
        tweet.source,
        tweet.public_metrics['reply_count'],
        tweet.public_metrics['retweet_count'],
        tweet.public_metrics['like_count'],
    ] for tweet in response.data]

    tweets_df = pd.DataFrame(data=tweets_data, columns=[
        'id',
        'text',
        'language',
        'post_date',
        'user',
        'source',
        'comment_number',
        'retweet_number',
        'like_number'
    ])

    users_df = pd.DataFrame(data=users_data, columns=[
        'id',
        'twitter_name',
        'username',
        'created_at',
    ])

    tweets_df.drop_duplicates(subset=['id'], inplace=True)
    users_df.drop_duplicates(subset=['id'], inplace=True)

    return tweets_df, users_df

def update_or_create_tweets_and_users_from_df(tweets_df, users_df, company=None):
    tweets = []
    for i in range(len(users_df)):
        user_from_df = users_df.loc[i,:]
        twitter_user, created = TwitterUser.objects.get_or_create(
            id = user_from_df.id
        )
        twitter_user.name = user_from_df.twitter_name
        twitter_user.username = user_from_df.username
        twitter_user.created_at = user_from_df.created_at
        twitter_user.save()

    for i in range(len(tweets_df)):
        tweet_from_df = tweets_df.loc[i,:]
        tweet = Tweet.objects.filter(
            id = tweet_from_df.id,
            post_date = tweet_from_df.post_date,
        )
        if len(tweet) > 0:
            tweet = tweet.first()
        else:
            tweet = Tweet.objects.create(
                id = tweet_from_df.id,
                post_date = tweet_from_df.post_date,
                user_id = tweet_from_df.user
            )
        tweet.user_id = tweet_from_df.user
        tweet.text = tweet_from_df.text
        tweet.language = tweet_from_df.language
        tweet.retweet_number = tweet_from_df.retweet_number
        tweet.comment_number = tweet_from_df.comment_number
        tweet.like_number = tweet_from_df.like_number
        tweet.source = tweet_from_df.source

        if company:
            tweet.companies.add(company)
        tweet.save()
        tweets.append(tweet)

    get_and_create_hashtags(tweets)
    TwitterUser.objects.annotate(t_count=Count('tweets')).filter(t_count=0).delete()


def get_tweets_by_hashtag(hashtag, MAX_TWEETS=100):
    response = Client.search_recent_tweets(
        query=f'{hashtag} new -is:retweet lang:en', 
        expansions=['author_id'],
        tweet_fields=['created_at', 'lang', 'author_id', 'public_metrics', 'source', 'entities'], # TODO context_annotations # TODO A lot of info!!!
        user_fields=['created_at', 'username', 'name'],
        since_id=None,
        sort_order='relevancy',
        max_results=MAX_TWEETS,
    )

    if response.meta['result_count'] == 0:
        return pd.DataFrame(), pd.DataFrame()

    return process_api_response(response)


def get_or_update_tweets_for_company(company, number_of_search_hashtags=5):
    hashtags = company.get_search_hashtags(number_of_search_hashtags)

    for hashtag in hashtags:
        tweets_df, users_df = get_tweets_by_hashtag(hashtag)

        if tweets_df.empty:
            continue

        update_or_create_tweets_and_users_from_df(tweets_df, users_df, company)


def update_tweets(tweets):
    response = Client.get_tweets(
        ids=[tweet.id for tweet in tweets],
        expansions=['author_id'],
        tweet_fields=['created_at', 'lang', 'author_id', 'public_metrics', 'source'],
        user_fields=['created_at', 'username', 'name'],
    )

    tweets_df, users_df = process_api_response(response)
    update_or_create_tweets_and_users_from_df(tweets_df, users_df)