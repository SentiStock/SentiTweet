import os

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from tweet.models import HashTag, Tweet


def get_sentiment(tweets):
    # TODO get tweet sentiment
    pass

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


def find_optimal_clusters_sse(text, max_k):
    iters = range(2, max_k+1, 1)
    
    sse = []
    for k in iters:
        sse.append(MiniBatchKMeans(n_clusters=k, init_size=1024, batch_size=2048, random_state=20).fit(text).inertia_)
        print('Fit {} clusters'.format(k))
        
    f, ax = plt.subplots(1, 1)
    ax.plot(iters, sse, marker='o')
    ax.set_xlabel('Cluster Centers')
    ax.set_xticks(iters)
    ax.set_xticklabels(iters)
    ax.set_ylabel('SSE')
    ax.set_title('SSE by Cluster Center Plot')
    plt.savefig('sentitweet/data/clusters_find.png')
    # plt.show()


def create_clusters(text, n_clusters):
    clusters = MiniBatchKMeans(n_clusters=n_clusters, init_size=1024, batch_size=2048, random_state=20).fit_predict(text)
    return clusters


def plot_clusters(data, labels):
    max_label = max(labels)
    max_items = np.random.choice(range(data.shape[0]), size=3000, replace=False)
    
    pca = PCA(n_components=2).fit_transform(data[max_items,:].todense())
    tsne = TSNE().fit_transform(PCA(n_components=50).fit_transform(data[max_items,:].todense()))
    
    idx = np.random.choice(range(pca.shape[0]), size=300, replace=False)
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
    for i,r in df.iterrows():
        print('\nCluster {}'.format(i))
        print(','.join([labels[t] for t in np.argsort(r)[-n_terms:]]))


def cluster(df):
    find_optimal_clusters_sse(text, 20)
    plot_tsne_pca(text, clusters)
    get_top_keywords(text, clusters, tfidf.get_feature_names(), 10)