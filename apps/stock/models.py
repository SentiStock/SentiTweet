import datetime

from authentication.models import FavoritesModelMixin
from django.db import models
from django.db.models import Count, Q, Sum
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
        return self.newest_tweet.post_date > (timezone.now() - datetime.timedelta(7)) if self.newest_tweet else False

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
        print(self.tweets.aggregate(Sum('like_number')))
        return self.tweets.aggregate(Sum('like_number'))['like_number__sum']

    @property
    def total_retweets(self):
        return self.tweets.aggregate(Sum('retweet_number'))['retweet_number__sum']

    @property
    def total_comments(self):
        return self.tweets.aggregate(Sum('comment_number'))['comment_number__sum']

    def get_tweets(self, from_date_time=None, till_date_time=None):
        if not from_date_time:
            from_date_time = self.oldest_tweet.post_date
        if not till_date_time:
            till_date_time = self.newest_tweet.post_date
        return self.tweets.filter(
            Q(post_date__gte=from_date_time) & Q(post_date__lte=till_date_time)
        )

    def get_compound(self, from_date_time=None, till_date_time=None):
        tweets = self.get_tweets(from_date_time, till_date_time)
        return tweets.aggregate(Avg('sentiment_compound'))['sentiment_compound__avg']