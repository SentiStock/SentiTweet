from stock.models import Company
from tweet.models import Tweet
from tweet.utils import get_sentiment

from sentitweet.twitter_api import get_or_update_tweets_for_company


def fetch_new_tweets():
    for company in Company.objects.all():
        get_or_update_tweets_for_company(company)

def tweet_score_sentiment():
    get_sentiment(Tweet.objects.filter(sentiment_compound=None).filter(like_number__gte=50))
