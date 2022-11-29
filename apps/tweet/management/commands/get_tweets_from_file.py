import os
import time
from datetime import datetime

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from stock.models import Company
from tweet.models import HashTag, Tweet, TwitterUser

from sentitweet.utils import create_from_df, get_sql_engine


class Command(BaseCommand):

    help = "Get tweets from file"

    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true', 
            help='When enabled, it deletes all already existing \
                Companies, Tweets, and TwitterUsers'
        )

    def handle(self, *args, **options):
        NUMBER_OF_TWEETS = 10000

        self.stdout.write(self.style.NOTICE('Gathering tweets from file...'))

        if options['delete']:
            self.stdout.write(self.style.NOTICE('Deleting current models...'))
            Tweet.objects.all().delete()
            Company.objects.all().delete()
            TwitterUser.objects.all().delete()
            HashTag.objects.all().delete()

        # COMPANIES
        self.stdout.write(self.style.NOTICE('Reading companies...'))
        companies = pd.read_csv('sentitweet/data/Company.csv')

        companies.rename(columns={
            'company_name':'name', 
            'ticker_symbol':'symbol'
            }, inplace=True
        )
        companies['id'] = [i for i in range(len(companies))]

        create_from_df(Company, companies)


        # COMPANY TWEETS & TWEETS
        start = time.time()
        self.stdout.write(self.style.NOTICE('Reading company_tweets...'))
        company_tweets = pd.read_csv('sentitweet/data/Company_Tweet.csv')
        self.stdout.write(self.style.NOTICE('Reading tweets...'))
        tweets = pd.read_csv('sentitweet/data/Tweet.csv')

        # Get requested number of tweets
        if NUMBER_OF_TWEETS:
            company_tweets = company_tweets.loc[:NUMBER_OF_TWEETS]
            tweets = tweets.loc[tweets.tweet_id.isin(list(company_tweets.tweet_id)),:]

        print(f'There are {len(company_tweets)} tweets to upload')

        # Assign teh correct company
        company_tweets.rename(columns={
            'ticker_symbol':'company_id',
            'tweet_id':'id',
        }, inplace=True)
        companies = Company.objects.all()
        company_tweets['company_id'] = company_tweets['company_id'].apply(
            lambda x: companies.get(symbol=x).id)

        # Rename tweets columns
        tweets.rename(columns={
            'tweet_id':'id',
            'writer':'user_id',
            'post_date':'post_date',
            'body':'text',
            'comment_num':'comment_number',
            'retweet_num':'retweet_number',
            'like_num': 'like_number'
            }, inplace=True
        )

        # Merge dataframes
        tweets = company_tweets.merge(tweets[[
            'id', 
            'user_id', 
            'post_date', 
            'text',
            'comment_number',
            'retweet_number',
            'like_number',
        ]], on = 'id', how = 'left')

        tweets.drop_duplicates(subset=["id"], inplace=True)

        twitter_users = tweets.iloc[:,2:3]
        twitter_users.rename(columns={'user_id':'name'}, inplace=True)
        twitter_users.drop_duplicates(inplace=True)
        twitter_users['id'] = [i for i in range(len(twitter_users))]

        tweets['post_date'] = tweets['post_date'].apply(lambda x: datetime.fromtimestamp(x))
        tweets['user_id'] = tweets['user_id'].apply(
            lambda x: twitter_users[twitter_users['name'] == x]['id'].values[0] 
            if not twitter_users[twitter_users['name'] == x].empty else 0
        )

        # TODO sentimetn and clean text

        tweets['cleaned_text'] = ''
        tweets['sentiment_pos'] = 0
        tweets['sentiment_neu'] = 0
        tweets['sentiment_neg'] = 0
        tweets['sentiment_compound'] = 0

        create_from_df(TwitterUser, twitter_users)
        create_from_df(Tweet, tweets)

        print(f'Tweets took: {time.time()-start} seconds')

        self.stdout.write(self.style.SUCCESS(
            'Finished gathering tweets from file'))