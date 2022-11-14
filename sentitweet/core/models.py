from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class TwitterUser(models.Model):
    name = models.CharField(max_length=255)

class Company(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=31)

class Tweet(models.Model):
    companies = models.ManyToManyField(Company)
    id = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(TwitterUser, on_delete=models.PROTECT)
    post_date = models.DateTimeField()
    text = models.TextField()
    comment_number = models.PositiveIntegerField()
    retweet_number = models.PositiveIntegerField()
    like_number = models.PositiveIntegerField()

class HashTag(models.Model):
    tweet = models.ManyToManyField(Tweet)
    companies = models.ManyToManyField(Company)
    value = models.CharField(max_length=255)

class Stock(models.Model):
    comapany = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    volume = models.PositiveIntegerField()
    open = models.PositiveIntegerField()
    close = models.PositiveIntegerField()
    high = models.PositiveIntegerField()
    low = models.PositiveIntegerField()