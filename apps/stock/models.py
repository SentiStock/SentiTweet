from django.db import models

from sentitweet.utils import get_sql_engine


class Company(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=31)

    def __str__(self):
        return self.name


class Stock(models.Model):
    comapany = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='stocks')
    date = models.DateField()
    volume = models.PositiveIntegerField()
    open = models.PositiveIntegerField()
    close = models.PositiveIntegerField()
    high = models.PositiveIntegerField()
    low = models.PositiveIntegerField()