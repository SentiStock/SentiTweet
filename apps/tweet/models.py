import pandas as pd
from django.core import serializers
from django.db import models
from stock.models import Company
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager


class PandasModelMixin(models.Model):
    @classmethod
    def as_dataframe(cls, queryset=None, field_list=None):
        if queryset is None:
            queryset = cls.objects.all()
        if field_list is None:
            field_list = [_field.name for _field in cls._meta._get_fields(reverse=False)]

        data = []
        [data.append([obj.serializable_value(column) for column in field_list]) for obj in queryset]

        columns = field_list

        df = pd.DataFrame(data, columns=columns)
        return df

    class Meta:
        abstract = True


class TwitterUser(PandasModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class HashTag(models.Model):
    companies = models.ManyToManyField(Company, related_name='hashtags')
    value = models.CharField(max_length=255)

    @property
    def tweets(self):
        from itertools import chain
        return set(chain(
            self.tweets0.all(),
            self.tweets1.all(),
            self.tweets2.all(),
            self.tweets3.all(),
            self.tweets4.all(),
            self.tweets5.all(),
            self.tweets6.all(),
            self.tweets7.all(),
            self.tweets8.all(),
            self.tweets9.all(),
        ))

    def __str__(self):
        return self.value


class Tweet(PandasModelMixin):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='tweets')
    user = models.ForeignKey(TwitterUser, on_delete=models.PROTECT, related_name='tweets')
    post_date = TimescaleDateTimeField(interval="1 day")
    text = models.TextField()
    cleaned_text = models.TextField(null=True, blank=True)
    comment_number = models.PositiveIntegerField(default=0)
    retweet_number = models.PositiveIntegerField(default=0)
    like_number = models.PositiveIntegerField(default=0)
    source = models.CharField(max_length=255, null=True, blank=True)

    sentiment_pos = models.IntegerField(default=0)
    sentiment_neu = models.IntegerField(default=0)
    sentiment_neg = models.IntegerField(default=0)
    sentiment_compound = models.IntegerField(default=0)

    hashtag0 = models.ForeignKey(HashTag, on_delete=models.PROTECT, related_name='tweets0', null=True, blank=True)
    hashtag1 = models.ForeignKey(HashTag, on_delete=models.PROTECT, related_name='tweets1', null=True, blank=True)
    hashtag2 = models.ForeignKey(HashTag, on_delete=models.PROTECT, related_name='tweets2', null=True, blank=True)
    hashtag3 = models.ForeignKey(HashTag, on_delete=models.PROTECT, related_name='tweets3', null=True, blank=True)
    hashtag4 = models.ForeignKey(HashTag, on_delete=models.PROTECT, related_name='tweets4', null=True, blank=True)
    hashtag5 = models.ForeignKey(HashTag, on_delete=models.PROTECT, related_name='tweets5', null=True, blank=True)
    hashtag6 = models.ForeignKey(HashTag, on_delete=models.PROTECT, related_name='tweets6', null=True, blank=True)
    hashtag7 = models.ForeignKey(HashTag, on_delete=models.PROTECT, related_name='tweets7', null=True, blank=True)
    hashtag8 = models.ForeignKey(HashTag, on_delete=models.PROTECT, related_name='tweets8', null=True, blank=True)
    hashtag9 = models.ForeignKey(HashTag, on_delete=models.PROTECT, related_name='tweets9', null=True, blank=True)

    objects = models.Manager()
    timescale = TimescaleManager()

    def __str__(self):
        return self.id

