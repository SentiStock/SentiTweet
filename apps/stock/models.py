import datetime

from authentication.models import FavoritesModelMixin
from django.conf import settings
from django.db import models
from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone
from tweet import models as tweet_models

from sentitweet.utils import get_sql_engine


class Company(FavoritesModelMixin):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=31)
    market_cap = models.BigIntegerField(null=True, blank=True)
    stock_price = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=63, null=True, blank=True)
    twitter_query_set = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_search_hashtags(self, top=10):
        name = self.search_name

        filtered_hashtags = self.hashtags.filter(
            value__icontains=name
        ).exclude(
            Q(value__icontains=':')
            | Q(value__icontains=')')
            | Q(value__icontains='(')
            | Q(value__icontains='"')
        )
        return filtered_hashtags.annotate(t_count=Count('tweets')).order_by('-t_count')[:top]

    def get_top_hashtags(self, top=10):
        return self.hashtags.annotate(t_count=Count('tweets')).order_by('-t_count')[:top]

    @property
    def search_name(self):
        return self.name.split(' ')[0].split('.')[0]

    @property
    def newest_tweet(self):
        return self.tweets.order_by('-post_date').first()

    @property
    def oldest_tweet(self):
        return self.tweets.order_by('-post_date').last()

    @property
    def is_up_to_date(self):
        return self.newest_tweet.post_date > (timezone.now() - datetime.timedelta(settings.DAYS_TILL_TWEETS_ARE_OUTDATED)) if self.newest_tweet else False

    @property
    def twitter_users(self):
        return tweet_models.TwitterUser.objects.filter(
            id__in=list(self.tweets.values_list('user_id', flat=True).distinct())
        )

    @property
    def top_twitter_users(self, top=10):
        return self.twitter_users.annotate(t_count=Count('tweets')).order_by('-t_count')[:top]

    @property
    def total_likes(self):
        return self.tweets.aggregate(Sum('like_number'))['like_number__sum']

    @property
    def total_retweets(self):
        return self.tweets.aggregate(Sum('retweet_number'))['retweet_number__sum']

    @property
    def total_comments(self):
        return self.tweets.aggregate(Sum('comment_number'))['comment_number__sum']

    def get_tweets(self, from_date_time=None, till_date_time=None):
        if not from_date_time:
            from_date_time = self.oldest_tweet.post_date if self.oldest_tweet else timezone.now()
        if not till_date_time:
            till_date_time = self.newest_tweet.post_date if self.newest_tweet else timezone.now()
        return self.tweets.filter(
            Q(post_date__gte=from_date_time) & Q(post_date__lte=till_date_time)
        )

    def get_compound(self, from_date_time=None, till_date_time=None):
        tweets = self.get_tweets(from_date_time, till_date_time)
        compound = tweets.aggregate(Avg('sentiment_compound'))['sentiment_compound__avg']
        if compound:
            return round(compound, 2)
        return 0

    def get_sentiment_label(self, from_date_time=None, till_date_time=None):
        compound = self.get_compound(from_date_time, till_date_time)
        if compound > settings.SENTIMENT_COMPOUND_TRHESHOLD:
            return 'positive'
        if compound < settings.SENTIMENT_COMPOUND_TRHESHOLD * -1:
            return 'negative'
        return 'neutral'

    def get_hashtags(self, from_date_time=None, till_date_time=None):
        tweets = self.get_tweets(from_date_time, till_date_time)
        hashtag_ids = set(tweets.values_list('hashtags', flat=True).distinct())
        return self.hashtags.filter(id__in=hashtag_ids)

    def get_twitter_users(self, from_date_time=None, till_date_time=None):
        from tweet.models import TwitterUser
        tweets = self.get_tweets(from_date_time, till_date_time)
        user_ids = set(tweets.values_list('user', flat=True).distinct())
        return TwitterUser.objects.filter(id__in=user_ids)