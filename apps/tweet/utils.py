import json
import os

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import requests
from django.conf import settings
from nltk.corpus import stopwords
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from tweet.models import HashTag, Tweet


def get_sentiment(all_tweets):
    headers = {
        "Content-Type": "application/json; charset=utf-8", 
        "x-functions-key": settings.SENTITWEETAPI_SENTIMENT_X_FUNCTIONS_KEY
    }
    print(len(all_tweets))
    for i in range(0, len(all_tweets), 600):
        tweets = all_tweets[i:i+600]
    
        data = {"tweets": [{"id": tweet.id, "text": tweet.text} for tweet in tweets]}
        
        response = requests.post(settings.SENTITWEETAPI_SENTIMENT_URL, headers=headers, json=data)
        print(response)
        for scored_tweet in json.loads(response._content):
            try:
                tweet_to_score = all_tweets.get(id=scored_tweet[0])
                tweet_to_score.sentiment_positive = scored_tweet[1]['positive']
                tweet_to_score.sentiment_negative = scored_tweet[1]['negative']
                tweet_to_score.sentiment_neutral = scored_tweet[1]['neutral']
                tweet_to_score.sentiment_compound = scored_tweet[1]['compound']
                tweet_to_score.sentiment_uncertain = scored_tweet[1]['uncertain']
                tweet_to_score.save()
            except Exception as e:
                continue
    
    return tweets
        

def get_and_create_hashtags(tweets):
    for tweet in tweets:
        hashtags = [j for j in [i for i in tweet.text.split() if i.startswith('#')]]
        for hashtag in hashtags:
            tag, created = HashTag.objects.get_or_create(value=hashtag)
            tag.tweets.add(tweet)
            [tag.companies.add(i) for i in tweet.companies.all()]
            tag.save()


def clean_tweet_text(text):
    stemmer = nltk.stem.SnowballStemmer('english', ignore_stopwords=True)
    stop_words = list(set(stopwords.words('english')))
    whitelist = set('abcdefghijklmnopqrstuvwxyz# ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    clean_text = text.replace("<br>", " ")
    clean_text = clean_text.replace("\n", " ")
    clean_text = clean_text.encode('ascii', 'ignore').decode('ascii')
    clean_text = ''.join(i + ' ' for i in clean_text.split() if not i.startswith('http') and not i.startswith('@'))
    clean_text = ''.join(i + ' ' for i in [stemmer.stem(word) for word in clean_text.lower().split() if word not in stop_words])
    return ''.join(filter(whitelist.__contains__, clean_text))


def clean_tweets(tweets):
    for tweet in tweets:
        tweet.cleaned_text = clean_tweet_text(tweet.text)
        tweet.save()


def get_vectorizer():
    tfidf = TfidfVectorizer(
        min_df = 5,
        max_df = 0.95,
        #max_features = 10000,
        stop_words = 'english'
    )
    return tfidf


def find_optimal_clusters_silh_score(text, max_k, plot=False):
    iters = range(2, max_k+1, 1)
    
    scores = {}
    for k in iters:
        model = MiniBatchKMeans(n_clusters=k, init_size=1024, batch_size=2048, random_state=20).fit(text)
        scores[k] = silhouette_score(text, model.labels_, metric='euclidean')

    if plot:
        f, ax = plt.subplots(1, 1)
        ax.plot(iters, scores.values(), marker='o')
        ax.set_xlabel('Cluster Centers')
        ax.set_xticks(iters)
        ax.set_xticklabels(iters)
        ax.set_ylabel('Silhouette Score')
        ax.set_title('Silhouette Score by Cluster Center Plot')
        plt.savefig('sentitweet/data/clusters_find.png')

    return max(scores, key=scores.get)


def find_optimal_clusters_sse(text, max_k):
    iters = range(2, max_k+1, 1)
    
    sse = []
    for k in iters:
        model = MiniBatchKMeans(n_clusters=k, init_size=1024, batch_size=2048, random_state=20).fit(text)
        print('Fit {} clusters'.format(k))
        sse.append(model.inertia_)

    f, ax = plt.subplots(1, 1)
    ax.plot(iters, sse, marker='o')
    ax.set_xlabel('Cluster Centers')
    ax.set_xticks(iters)
    ax.set_xticklabels(iters)
    ax.set_ylabel('SSE')
    ax.set_title('SSE by Cluster Center Plot')
    plt.savefig('sentitweet/data/clusters_find.png')


def create_model(text, n_clusters):
    model = MiniBatchKMeans(n_clusters=n_clusters, init_size=1024, batch_size=2048, random_state=20)
    model = model.fit(text)
    return model

def model_predict(model, text):
    clusters = model.predict(text)
    return clusters

def get_most_repr_tweets(model, tweets, text, number_of_top_tweets=3):
    centers = model.cluster_centers_
    text = text.toarray()
    final = [['', np.inf] for i in range(len(centers))]

    distance = []

    for i in range(len(tweets)):
        tweet = tweets.loc[i,:]
        dist = np.linalg.norm(centers[tweet.cluster], text[i][0])
        distance.append(dist)

    tweets['dist'] = distance

    groups = tweets.sort_values('dist', ascending=True).groupby('cluster').head(number_of_top_tweets)
    return groups


def plot_clusters(data, labels):
    max_label = max(labels)
    max_items = np.random.choice(range(data.shape[0]), size=int(len(labels)/5), replace=False)
    
    pca = PCA(n_components=2).fit_transform(data[max_items,:].todense())
    tsne = TSNE().fit_transform(PCA(n_components=50).fit_transform(data[max_items,:].todense()))
    
    idx = np.random.choice(range(pca.shape[0]), size=int(len(labels)/50), replace=False)
    label_subset = labels[max_items]
    label_subset = [cm.hsv(i/max_label) for i in label_subset[idx]]
    
    f, ax = plt.subplots(1, 2, figsize=(14, 6))
    
    ax[0].scatter(pca[idx, 0], pca[idx, 1], c=label_subset)
    ax[0].set_title('PCA Cluster Plot')
    
    ax[1].scatter(tsne[idx, 0], tsne[idx, 1], c=label_subset)
    ax[1].set_title('TSNE Cluster Plot')

    plt.savefig('sentitweet/data/clusters_create.png')


def get_top_keywords(data, clusters, labels, n_terms):
    df = pd.DataFrame(data.todense()).groupby(clusters).mean()

    key_words = {}
    for i,r in df.iterrows():
        key_words[i] = [labels[t] for t in np.argsort(r)[-n_terms:]]

    return key_words

def get_cluster_info(tweets):
    grouped_df = tweets.groupby([tweets['cluster']])
    final_df = pd.DataFrame()
    final_df['count'] = grouped_df['id'].count()
    final_df['like_number'] = grouped_df['like_number'].sum()
    final_df['retweet_number'] = grouped_df['retweet_number'].sum()
    final_df['comment_number'] = grouped_df['comment_number'].sum()
    final_df['sentiment_compound'] = grouped_df['sentiment_compound'].mean()
    return final_df

def cluster_tweets(tweets, max_k=10, number_of_best_tweets=3):
    if not isinstance(tweets, pd.DataFrame):
        tweets = Tweet.as_dataframe(queryset=tweets)

    if len(tweets) == 0:
        return None, {}
        # raise Exception(f'There are no tweets in this queryset...')
        
    tweets.drop_duplicates(subset=["cleaned_text"], inplace=True)
    tweets.reset_index(inplace=True, drop=True)

    tfidf = get_vectorizer()
    tfidf.fit(tweets.cleaned_text)
    text = tfidf.transform(tweets.cleaned_text)

    number_of_clusters = find_optimal_clusters_silh_score(text, max_k=max_k)

    model = create_model(text, number_of_clusters)
    clusters = model_predict(model, text)
    tweets['cluster'] = clusters

    best_tweets = get_most_repr_tweets(model, tweets, text, number_of_best_tweets)
    top_words = get_top_keywords(text, clusters, tfidf.get_feature_names(), 10)
    info = get_cluster_info(tweets)

    return best_tweets, top_words, info
