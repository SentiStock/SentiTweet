import os
import tweepy

bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
Client = tweepy.Client(bearer_token)


def get_tweets_by_hashtag(hashtag):
    MAX_TWEETS = 10
    # tweets = tweepy.Cursor(
    #     twitter_api.search_tweets,
    #     q=f'{hashtag} -filter:retweets',
    #     tweet_mode='extended'
    # ).items(MAX_TWEETS)

    response = Client.search_recent_tweets(query=f'{hashtag}', max_results=MAX_TWEETS)

    print(response.data)

    tweets_data = [[
        tweet.id,
        tweet.full_text,
        tweet.lang,
        tweet.created_at,
        tweet.user.id,
        tweet.user.location,
    ] for tweet in response.data]

    df = pd.DataFrame(data=tweets_data, columns=[
        'id',
        'text',
        'language',
        'post_date',
        'user_id',
        'user_location',
        'geo_location'
    ])

    df.rename(columns={'ticker_symbol':'company_id'}, inplace=True)

    return df

def get_tweets_for_company(company):
    hashtags = company.hashtags.all()
    for hashtag in hashtags:
        get_tweets_by_hashtag(hashtag)