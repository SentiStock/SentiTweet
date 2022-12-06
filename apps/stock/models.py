import datetime

from authentication.models import FavoritesModelMixin
from django.db import models
from django.db.models import Count, Q
from django.utils import timezone
from tweet import models as tweet_models

from sentitweet.utils import get_sql_engine


class Company(FavoritesModelMixin):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=31)

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
    def is_up_to_date(self):
        return self.newest_tweet.post_date > (timezone.now() - datetime.timedelta(7))

    @property
    def contributers(self):
        return tweet_models.TwitterUser.objects.filter(
            id__in=list(self.tweets.values_list('user_id', flat=True).distinct())
        )


class Stock(models.Model):
    comapany = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='stocks')
    date = models.DateField()
    volume = models.PositiveIntegerField()
    open = models.PositiveIntegerField()
    close = models.PositiveIntegerField()
    high = models.PositiveIntegerField()
    low = models.PositiveIntegerField()