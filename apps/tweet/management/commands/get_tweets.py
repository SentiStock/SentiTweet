import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from sentitweet.twitter_api import get_tweets_by_hashtag


class Command(BaseCommand):

    help = "Get tweets from twitter"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(
            'Gathering tweets from twitter...'))

        # try:
        print(get_tweets_by_hashtag('#TSLA'))
            # TODO code to get and store 

        # except Exception as e:
            # self.stdout.write(f'Something went wrong: {e}')

        self.stdout.write(self.style.SUCCESS(
            'Successfully gathered tweets from twitter'))
