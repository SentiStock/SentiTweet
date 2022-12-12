import datetime
import os

import pandas as pd
import tweepy
from django.db.models import Count
from django.utils import timezone
from tweet.models import HashTag, Tweet, TwitterUser
from tweet.utils import clean_tweet_text, get_and_create_hashtags

from sentitweet.utils import create_from_df

bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
Client = tweepy.Client(bearer_token)#, return_type=dict)


def process_api_tweets(response):
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
    ] for tweet in response]

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

    tweets_df.drop_duplicates(subset=['id'], inplace=True)
    tweets_df.reset_index(inplace=True, drop=True)

    return tweets_df


def process_api_users(response):
    users_data = [[
        user.id,
        user.name,
        user.username,
        user.created_at
    ] for user in response.data]

    users_df = pd.DataFrame(data=users_data, columns=[
        'id',
        'twitter_name',
        'username',
        'created_at',
    ])

    users_df.drop_duplicates(subset=['id'], inplace=True)
    users_df.reset_index(inplace=True, drop=True)

    return users_df


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
        tweet.cleaned_text = clean_tweet_text(tweet_from_df.text)

        if company:
            tweet.companies.add(company)

        tweet.save()
        tweets.append(tweet)

    get_and_create_hashtags(tweets)
    TwitterUser.objects.annotate(t_count=Count('tweets')).filter(t_count=0).delete()


def get_users_by_ids(user_ids):
    users_df = pd.DataFrame()

    for i in range(0, len(user_ids), 100):
        response = Client.get_users(
            ids=user_ids[i:i+100],
            user_fields=[
                'created_at',
                'description',
                'entities',
                'id',
                'location',
                'name',
                'pinned_tweet_id',
                'profile_image_url',
                'protected',
                'public_metrics',
                'url',
                'username',
                'verified',
                'withheld'
            ],
        )
        users_df = pd.concat([users_df, process_api_users(response)], ignore_index=True)

    return users_df


def get_tweets_by_hashtag(hashtag, MAX_TWEETS=1000):
    if isinstance(hashtag, HashTag):
        since = hashtag.newest_tweet.id if hashtag.newest_tweet else None
        if since < (timezone.now() - datetime.timedelta(days=6)).timestamp():
            since = None
    else:
        since = None

    response = tweepy.Paginator(
        Client.search_recent_tweets,
        query=f'{hashtag} new -is:retweet lang:en', 
        expansions=['author_id'],
        tweet_fields=['created_at', 'lang', 'author_id', 'public_metrics', 'source'],#, 'entities', 'context_annotations'], # TODO context_annotations # TODO A lot of info!!!
        user_fields=['created_at', 'username', 'name'],
        sort_order='relevancy',
        max_results=100,
        # since_id=since,
    ).flatten(limit=MAX_TWEETS)

    return process_api_tweets(response)


def get_or_update_tweets_for_company(company, number_of_search_hashtags=5):
    hashtags = company.get_search_hashtags(number_of_search_hashtags)
    tweets_df = get_tweets_by_hashtag(company.search_name)

    if not tweets_df.empty:
        users_df = get_users_by_ids(list(tweets_df.user))
        update_or_create_tweets_and_users_from_df(tweets_df, users_df, company)

    for hashtag in hashtags:
        tweets_df = get_tweets_by_hashtag(hashtag)

        if tweets_df.empty:
            continue

        users_df = get_users_by_ids(list(tweets_df.user))
        update_or_create_tweets_and_users_from_df(tweets_df, users_df, company)


def update_tweets(tweets):
    response = Client.get_tweets(
        ids=[tweet.id for tweet in tweets],
        expansions=['author_id'],
        tweet_fields=['created_at', 'lang', 'author_id', 'public_metrics', 'source'],
        user_fields=['created_at', 'username', 'name'],
    )

    tweets_df, users_df = process_api_response(response) #FIXME
    update_or_create_tweets_and_users_from_df(tweets_df, users_df)