from django.conf import settings
from django.core.management.base import BaseCommand

from sentitweet.cron import tweet_score_sentiment


class Command(BaseCommand):

    help = "Score tweet sentiment"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(
            'Scoring tweet sentiment...'))

        tweet_score_sentiment()

        self.stdout.write(self.style.SUCCESS(
            'Successfully scored tweet sentiment'))
