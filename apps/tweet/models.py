import pandas as pd
from authentication.models import CustomUser, FavoritesModelMixin
from django.core import serializers
from django.db import models


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

    @property
    def newest_tweet(self):
        return self.tweets.order_by('-post_date').first()

    @property
    def oldest_tweet(self):
        return self.tweets.order_by('-post_date').last()

    def __str__(self):
        return self.name


class Tweet(PandasModelMixin):
    companies = models.ManyToManyField('stock.Company', related_name='tweets')
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


class HashTag(FavoritesModelMixin):
    tweets = models.ManyToManyField(Tweet, related_name='hashtags')
    companies = models.ManyToManyField('stock.Company', related_name='hashtags')
    value = models.CharField(max_length=255)

    @property
    def clean_value(self):
        return self.value[1:]

    @property
    def newest_tweet(self):
        return self.tweets.order_by('-post_date').first()

    @property
    def oldest_tweet(self):
        return self.tweets.order_by('-post_date').last()
        
    @property
    def contributers(self):
        return TwitterUser.objects.filter(
            id__in=list(self.tweets.values_list('user_id', flat=True).distinct())
        )

    @property
    def best_contributers(self, top=10):
        return self.contributers.annotate(t_count=Count('tweets')).order_by('-t_count')[:top]

    def __str__(self):
        return self.value


class Set(FavoritesModelMixin):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='sets')
    hashtags = models.ManyToManyField(HashTag, related_name='sets')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    MODE_CHOICES = (
        ('private', 'PRIVATE'),
        ('public', 'PUBLIC'),
    )
    mode = models.CharField(
        max_length = 20,
        choices = MODE_CHOICES,
        default = 'private'
    )

    @property
    def tweets(self):
        tweet_ids = set(self.hashtags.values_list('tweets', flat=True).distinct())
        return Tweet.objects.filter(id__in=tweet_ids)

    @property
    def newest_tweet(self):
        return self.tweets.order_by('-post_date').first()

    @property
    def oldest_tweet(self):
        return self.tweets.order_by('-post_date').last()

    @property
    def contributers(self):
        twitter_user_ids = set(self.tweets.values_list('user_id', flat=True).distinct())
        return TwitterUser.objects.filter(id__in=twitter_user_ids)
    
    @property
    def best_contributers(self, top=10):
        return self.contributers.annotate(t_count=Count('tweets')).order_by('-t_count')[:top]

    def __str__(self):
        return self.name