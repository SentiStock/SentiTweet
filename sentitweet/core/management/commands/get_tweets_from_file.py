import os
from datetime import datetime
import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from core.models import Company, Tweet, TwitterUser


class Command(BaseCommand):

    help = "Get tweets from file"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Gathering tweets from file...'))

        # COMPANIES
        try:
            self.stdout.write(self.style.NOTICE('Reading companies...'))
            companies = pd.read_csv('sentitweet/data/Company.csv')
            for i in range(len(companies)):
                Company.objects.get_or_create(
                    name=companies.loc[i, 'company_name'], 
                    symbol=companies.loc[i, 'ticker_symbol']
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Something went wrong with Company.csv: {e}'))
        
        # TWEETS
        try:
            self.stdout.write(self.style.NOTICE('Reading tweets...'))
            tweets = pd.read_csv('sentitweet/data/Tweet.csv')
            for i in range(len(tweets)):
                user, created = TwitterUser.objects.get_or_create(
                    name=tweets.loc[i, 'writer']
                )
                post_date = datetime.fromtimestamp(tweets.loc[i, 'post_date'])
                Tweet.objects.get_or_create(
                    id=tweets.loc[i, 'tweet_id'],
                    user=user,
                    post_date=post_date,
                    text=tweets.loc[i, 'body'],
                    comment_number=tweets.loc[i, 'comment_num'],
                    retweet_number=tweets.loc[i, 'retweet_num'],
                    like_number=tweets.loc[i, 'like_num'],
                )
                if i % 1000 == 0:
                    self.stdout.write(self.style.NOTICE(f'Tweet number: {i}/{len(tweets)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Something went wrong with Tweet.csv: {e}'))

        # COMPANY TWEETS
        try:
            self.stdout.write(self.style.NOTICE('Reading company_tweets...'))
            company_tweets = pd.read_csv('sentitweet/data/Company_Tweet.csv')
            companies = Company.objects.all();
            tweets = Tweet.objects.all()
            for i in range(len(company_tweets)):
                company = companies.get(symbol=company_tweets.loc[i, 'ticker_symbol'])
                tweets.get(id=company_tweets.loc[i, 'tweet_id']).comapanies.add(company)

            if i % 1000 == 0:
                self.stdout.write(self.style.NOTICE(f'Company_Tweet number: {i}/{len(company_tweets)}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Something went wrong with Company_Tweet.csv: {e}'))
        

        self.stdout.write(self.style.SUCCESS(
            'Finished gathering tweets from file'))
