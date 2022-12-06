import pandas as pd
from django.core import serializers
from django.db import models
from stock.models import Company


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


class Tweet(PandasModelMixin):
    # id = models.BigIntegerField(primary_key=True)
    companies = models.ManyToManyField(Company, related_name='tweets')
    user = models.ForeignKey(TwitterUser, on_delete=models.PROTECT, related_name='tweets')
    post_date = models.DateTimeField()
    text = models.TextField()
    cleaned_text = models.TextField(null=True, blank=True)
    comment_number = models.PositiveIntegerField(default=0)
    retweet_number = models.PositiveIntegerField(default=0)
    like_number = models.PositiveIntegerField(default=0)
    source = models.CharField(max_length=255, null=True, blank=True)

    # sentiment = models.IntegerField()

    def __str__(self):
        return str(self.id)


class HashTag(models.Model):
    tweets = models.ManyToManyField(Tweet, related_name='hashtags')
    companies = models.ManyToManyField(Company, related_name='hashtags')
    value = models.CharField(max_length=255)

    @property
    def clean_value(self):
        return self.value[1:]

    def __str__(self):
        return self.value

