from django.conf import settings
from django.core.management.base import BaseCommand
from stock.models import Company

from sentitweet.twitter_api import (get_or_update_tweets_for_company,
                                    get_tweets_by_hashtag, update_tweets)


class Command(BaseCommand):

    help = "Get tweets from twitter"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(
            'Gathering tweets from twitter...'))

        update_tweets(Company.objects.first().tweets.all()[:10])

        # number_of_search_hashtags = 5

        # for company in Company.objects.all():
        #     print(f'gathering {company}')
        #     print([(i.value, i.tweets.count()) for i in company.get_search_hashtags(number_of_search_hashtags)])
        #     get_or_update_tweets_for_company(company, number_of_search_hashtags)

        # except Exception as e:
            # self.stdout.write(f'Something went wrong: {e}')

        self.stdout.write(self.style.SUCCESS(
            'Successfully gathered tweets from twitter'))
