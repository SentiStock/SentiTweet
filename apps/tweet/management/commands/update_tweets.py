from django.conf import settings
from django.core.management.base import BaseCommand
from tweet.models import Tweet

from sentitweet.twitter_api import update_tweets


class Command(BaseCommand):

    help = "update hashtags from all tweets"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(
            'Updating tweets...'))

        tweets = Tweet.objects.filter(source=None)
        length = len(tweets)
        self.stdout.write(self.style.NOTICE(
            f'There are {length} tweets to to be updated'))

        chunk_size = 100
        for i in range(0, length, chunk_size):
            print(f'{i}/{length}')
            try:
                update_tweets(tweets[i:i+chunk_size])
            except Exception as e:
                print(f'something went wrong with chunck {i}-{i+chunk_size}/{length} probably because we do not have permission:', e)

        self.stdout.write(self.style.SUCCESS(
            'Successfully updated all tweets'))
