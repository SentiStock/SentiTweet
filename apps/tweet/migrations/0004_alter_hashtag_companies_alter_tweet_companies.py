# Generated by Django 4.1.3 on 2022-11-23 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_alter_stock_comapany_delete_customuser'),
        ('tweet', '0003_tweet_cleaned_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='companies',
            field=models.ManyToManyField(related_name='hashtags', to='stock.company'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='companies',
            field=models.ManyToManyField(related_name='tweets', to='stock.company'),
        ),
    ]