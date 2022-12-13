from rest_framework import serializers
from stock.models import Company
from tweet.models import HashTag, Set, Tweet, TwitterUser


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    tweet_count = serializers.ReadOnlyField()
    hashtag_count = serializers.ReadOnlyField()
    twitter_user_count = serializers.ReadOnlyField()
    favorite_count = serializers.ReadOnlyField()
    is_up_to_date = serializers.ReadOnlyField()
    newest_tweet = TweetSerializer(read_only=True)

    class Meta:
        model = Company
        fields = '__all__'
        

class HashTagSerializer(serializers.ModelSerializer):
    clean_value = serializers.ReadOnlyField()
    tweet_count = serializers.ReadOnlyField()
    twitter_user_count = serializers.ReadOnlyField()
    favorite_count = serializers.ReadOnlyField()
    is_up_to_date = serializers.ReadOnlyField()
    newest_tweet = TweetSerializer(read_only=True)

    class Meta:
        model = HashTag
        fields = '__all__'

class SetSerializer(serializers.ModelSerializer):
    tweet_count = serializers.ReadOnlyField()
    hashtag_count = serializers.ReadOnlyField()
    twitter_user_count = serializers.ReadOnlyField()
    favorite_count = serializers.ReadOnlyField()
    is_up_to_date = serializers.ReadOnlyField()
    newest_tweet = TweetSerializer(read_only=True)

    class Meta:
        model = Set
        fields = '__all__'

class TwitterUserSerializer(serializers.ModelSerializer):
    tweet_count = serializers.ReadOnlyField()
    favorite_count = serializers.ReadOnlyField()
    is_up_to_date = serializers.ReadOnlyField()
    newest_tweet = TweetSerializer(read_only=True)

    class Meta:
        model = TwitterUser
        fields = '__all__'