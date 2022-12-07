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

    help = "Get companies from file"

    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true', 
            help='When enabled, it deletes all already existing Companies'
        )
        parser.add_argument('-n', '--number', type=int, help='Get the first n companies from the files')


    def handle(self, *args, **options):
        NUMBER_OF_COMPANIES = None
        if options['number']:
            NUMBER_OF_COMPANIES = options['number']

        self.stdout.write(self.style.NOTICE('Gathering companies from file...'))

        if options['delete']:
            self.stdout.write(self.style.NOTICE('Deleting current companies...'))
            Company.objects.all().delete()

        # COMPANIES
        self.stdout.write(self.style.NOTICE('Reading companies...'))
        companies = pd.read_csv('sentitweet/data/companies.csv')

        if NUMBER_OF_COMPANIES:
            companies = companies.loc[:NUMBER_OF_COMPANIES]

        companies.rename(columns={
            'STOCK': 'company_name',
            'SYMBOL': 'symbol',
            'MARKETCAP': 'market_cap',
            'PRICE': 'stock_price',
            'COUNTRY': 'country',
        }, inplace=True)
        companies['id'] = [i for i in range(len(companies))]

        for i in range(len(companies)):
            company_from_df = companies.loc[i,:]
            company, created = Company.objects.get_or_create(
                id = company_from_df.id,
                name = company_from_df.company_name,
                symbol = company_from_df.symbol,
                market_cap = company_from_df.market_cap,
                stock_price = company_from_df.stock_price,
                country = company_from_df.country,
            )

        self.stdout.write(self.style.SUCCESS(
            'Finished creating companies from file'))
