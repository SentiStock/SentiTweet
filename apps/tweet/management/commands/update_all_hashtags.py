from django.conf import settings
from django.core.management.base import BaseCommand
from tweet.models import Tweet
from tweet.utils import get_and_create_hashtags


class Command(BaseCommand):

    help = "update hashtags from all tweets"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(
            'Updating all hashtags...'))

        tweets = Tweet.objects.all()
        self.stdout.write(self.style.NOTICE(
            f'There are {len(tweets)} tweets to get hashtags from'))

        get_and_create_hashtags(Tweet.objects.all())

        self.stdout.write(self.style.SUCCESS(
            'Successfully updated all hashtags'))
