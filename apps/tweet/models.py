import datetime

import pandas as pd
from authentication.models import Contributor, FavoritesModelMixin
from django.conf import settings
from django.core import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone


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
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    joined_date = models.DateTimeField(null=True, blank=True)
    url = models.URLField(max_length=511, null=True, blank=True)
    verified = models.BooleanField(null=True, blank=True)

    followers_count = models.PositiveIntegerField(null=True, blank=True)
    following_count = models.PositiveIntegerField(null=True, blank=True)
    tweet_count = models.PositiveIntegerField(null=True, blank=True)
    listed_count = models.PositiveIntegerField(null=True, blank=True)
    # Entities TODO
    # Withheld TODO

    @property
    def tweet_count(self):
        return self.tweets.count()

    @property
    def favorite_count(self):
        return self.favorites.count()

    @property
    def newest_tweet(self):
        return self.tweets.order_by('-post_date').first()

    @property
    def oldest_tweet(self):
        return self.tweets.order_by('-post_date').last()

    @property
    def is_up_to_date(self):
        return self.newest_tweet.post_date > (timezone.now() - datetime.timedelta(settings.DAYS_TILL_TWEETS_ARE_OUTDATED)) if self.newest_tweet else False

    def total_likes(self, from_date_time=None, till_date_time=None):
        tweets = self.get_tweets(from_date_time, till_date_time)
        return tweets.aggregate(Sum('like_number'))['like_number__sum']

    def total_retweets(self, from_date_time=None, till_date_time=None):
        tweets = self.get_tweets(from_date_time, till_date_time)
        return tweets.aggregate(Sum('retweet_number'))['retweet_number__sum']

    def total_comments(self, from_date_time=None, till_date_time=None):
        tweets = self.get_tweets(from_date_time, till_date_time)
        return tweets.aggregate(Sum('comment_number'))['comment_number__sum']

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

    @property
    def sentiment_label(self):
        sentiment_compound = self.get_compound()
        if not sentiment_compound:
            return 'Undefined'
        if sentiment_compound > settings.SENTIMENT_COMPOUND_TRHESHOLD:
            return 'Positive'
        if sentiment_compound < settings.SENTIMENT_COMPOUND_TRHESHOLD * -1:
            return 'Negative'
        return 'Neutral'

    def __str__(self):
        return self.name


class Tweet(PandasModelMixin):
    id = models.BigIntegerField(primary_key=True)
    companies = models.ManyToManyField('stock.Company', related_name='tweets')
    user = models.ForeignKey(TwitterUser, on_delete=models.PROTECT, related_name='tweets')
    post_date = models.DateTimeField()
    source = models.CharField(max_length=255, null=True, blank=True)

    text = models.TextField()
    cleaned_text = models.TextField(null=True, blank=True)

    comment_number = models.PositiveIntegerField(null=True, blank=True)
    retweet_number = models.PositiveIntegerField(null=True, blank=True)
    like_number = models.PositiveIntegerField(null=True, blank=True)

    sentiment_positive = models.DecimalField(null=True, blank=True, 
        validators=[MinValueValidator(0), MaxValueValidator(1)], decimal_places=4, max_digits=5)
    sentiment_neutral = models.DecimalField(null=True, blank=True, 
        validators=[MinValueValidator(0), MaxValueValidator(1)], decimal_places=4, max_digits=5)
    sentiment_negative = models.DecimalField(null=True, blank=True, 
        validators=[MinValueValidator(0), MaxValueValidator(1)], decimal_places=4, max_digits=5)
    sentiment_uncertain = models.DecimalField(null=True, blank=True, 
        validators=[MinValueValidator(0), MaxValueValidator(1)], decimal_places=4, max_digits=5)
    sentiment_compound = models.DecimalField(null=True, blank=True, 
        validators=[MinValueValidator(-1), MaxValueValidator(1)], decimal_places=4, max_digits=5)

    @property
    def sentiment_label(self):
        if not self.sentiment_compound:
            return 'Undefined'
        if self.sentiment_compound > settings.SENTIMENT_COMPOUND_TRHESHOLD:
            return 'Positive'
        if self.sentiment_compound < settings.SENTIMENT_COMPOUND_TRHESHOLD * -1:
            return 'Negative'
        return 'Neutral'

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
    def total_likes(self):
        return self.tweets.aggregate(Sum('like_number'))['like_number__sum']

    @property
    def total_retweets(self):
        return self.tweets.aggregate(Sum('retweet_number'))['retweet_number__sum']

    @property
    def total_comments(self):
        return self.tweets.aggregate(Sum('comment_number'))['comment_number__sum']

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
        return TwitterUser.objects.filter(
            id__in=list(self.tweets.values_list('user_id', flat=True).distinct())
        )

    @property
    def top_twitter_users(self, top=10):
        return self.twitter_users.annotate(t_count=Count('tweets')).order_by('-t_count')[:top]

    def __str__(self):
        return self.value


class Set(FavoritesModelMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(Contributor, on_delete=models.PROTECT, related_name='sets')
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
    def total_likes(self):
        return self.tweets.aggregate(Sum('like_number'))['like_number__sum']

    @property
    def total_retweets(self):
        return self.tweets.aggregate(Sum('retweet_number'))['retweet_number__sum']

    @property
    def total_comments(self):
        return self.tweets.aggregate(Sum('comment_number'))['comment_number__sum']

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
        twitter_user_ids = set(self.tweets.values_list('user_id', flat=True).distinct())
        return TwitterUser.objects.filter(id__in=twitter_user_ids)
    
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

    def __str__(self):
        return self.name