from django.db import models
from django.db.models import Count, Q

from sentitweet.utils import get_sql_engine


class Company(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=31)

    def __str__(self):
        return self.name

    def get_search_hashtags(self, top=10):
        # TODO check if this is the right approach
        # TODO we could check if the word stock is in the hashtag + other keywords

        name = self.name
        if len(name.split(' ')) > 1:
            name = name.split(' ')[0]
        if len(name.split('.')) > 1:
            name = name.split('.')[0]

        filtered_hashtags = self.hashtags.filter(
            # Q(value__icontains=self.symbol)
            Q(value__icontains=name)
        ).exclude(
            Q(value__icontains=':')
            | Q(value__icontains=')')
            | Q(value__icontains='(')
            | Q(value__icontains='"')
        )
        return filtered_hashtags.annotate(t_count=Count('tweets')).order_by('-t_count')[:top]

    def get_top_hashtags(self, top=10):
        return self.hashtags.annotate(t_count=Count('tweets')).order_by('-t_count')[:top]


class Stock(models.Model):
    comapany = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='stocks')
    date = models.DateField()
    volume = models.PositiveIntegerField()
    open = models.PositiveIntegerField()
    close = models.PositiveIntegerField()
    high = models.PositiveIntegerField()
    low = models.PositiveIntegerField()