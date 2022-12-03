from stock.models import Company

from sentitweet.twitter_api import get_or_update_tweets_for_company


def fetch_new_tweets():
    for company in Company.objects.all():
        get_or_update_tweets_for_company(company)

