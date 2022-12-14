import os
import time
from datetime import datetime

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from stock.models import Company
from tweet.models import Tweet, TwitterUser
from tweet.utils import clean_tweet_text

from sentitweet.utils import create_from_df, get_sql_engine


class Command(BaseCommand):

    help = "Get tweets from file"

    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true', 
            help='When enabled, it deletes all already existing \
                Companies, Tweets, and TwitterUsers'
        )
        parser.add_argument('-n', '--number', type=int, help='Get the first n tweets from the files')


    def handle(self, *args, **options):
        NUMBER_OF_TWEETS = None
        if options['number']:
            NUMBER_OF_TWEETS = options['number']

        self.stdout.write(self.style.NOTICE('Gathering tweets from file...'))

        if options['delete']:
            self.stdout.write(self.style.NOTICE('Deleting current models...'))
            Tweet.objects.all().delete()
            Company.objects.all().delete()
            TwitterUser.objects.all().delete()

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

        # TWEETS
        start = time.time()
        self.stdout.write(self.style.NOTICE('Reading tweets...'))
        tweets = pd.read_csv('sentitweet/data/Tweet.csv')

        if NUMBER_OF_TWEETS:
            tweets = tweets.loc[:NUMBER_OF_TWEETS]
        print(f'There are {len(tweets)} tweets')

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
        tweets.drop_duplicates(subset=["id"], inplace=True)

        twitter_users = tweets.iloc[:,1:2]
        twitter_users.rename(columns={'user_id':'name'}, inplace=True)
        twitter_users.drop_duplicates(inplace=True)
        twitter_users['id'] = [i for i in range(len(twitter_users))]

        tweets['post_date'] = tweets['post_date'].apply(lambda x: datetime.fromtimestamp(x))
        tweets['user_id'] = tweets['user_id'].apply(
            lambda x: twitter_users[twitter_users['name'] == x]['id'].values[0] 
            if not twitter_users[twitter_users['name'] == x].empty else 0
        )
        tweets['cleaned_text'] = tweets['text'].apply(lambda x: clean_tweet_text(x))

        create_from_df(TwitterUser, twitter_users)
        create_from_df(Tweet, tweets)

        print(f'Tweets took: {time.time()-start} seconds')

        # COMPANY TWEETS
        start = time.time()
        self.stdout.write(self.style.NOTICE('Reading company_tweets...'))
        company_tweets = pd.read_csv('sentitweet/data/Company_Tweet.csv')

        if NUMBER_OF_TWEETS:
            company_tweets = company_tweets.loc[company_tweets.tweet_id.isin(list(tweets.id)),:]
        print(f'There are {len(company_tweets)} company_tweets')

        company_tweets.rename(columns = {'ticker_symbol':'company_id'}, inplace=True)
        company_tweets['id'] = [i for i in range(len(company_tweets))]

        companies = Company.objects.all()

        company_tweets['company_id'] = company_tweets['company_id'].apply(
            lambda x: companies.get(symbol=x).id)

        create_from_df(None, company_tweets, table='tweet_tweet_companies')

        print(f'Company_Tweet took: {time.time()-start} seconds')

        self.stdout.write(self.style.SUCCESS(
            'Finished gathering tweets from file'))
