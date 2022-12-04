from django.conf import settings
from django.core.management.base import BaseCommand
from tweet.models import Tweet
from tweet.utils import (create_model, get_most_repr_tweets, get_top_keywords,
                         get_vectorizer, model_predict, plot_clusters)


class Command(BaseCommand):

    help = "Create clusters and print common words"

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='Number of clusters to try')

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Creating clusters...'))

        number_of_clusters = options['number']

        tweets = Tweet.as_dataframe()
        tweets.drop_duplicates(subset=["cleaned_text"], inplace=True)
        tweets.reset_index(inplace=True, drop=True)
        print(f'Creating clusters for {len(tweets)} tweets')

        tfidf = get_vectorizer()
        tfidf.fit(tweets.cleaned_text)
        text = tfidf.transform(tweets.cleaned_text)

        model = create_model(text, number_of_clusters)
        clusters = model_predict(model, text)

        tweets['cluster'] = clusters

        best_tweets = get_most_repr_tweets(model, tweets, text)
        top_words = get_top_keywords(text, clusters, tfidf.get_feature_names(), 10)

        print('-'*50)
        print(best_tweets[['cluster', 'text', 'dist']])
        print('-'*50)

        print('Top key words for all the clusters are:')
        [print(k,v) for k,v in top_words.items()]

        plot_clusters(text, clusters)

        self.stdout.write(self.style.SUCCESS(
            'Successfully created clusters, saved as: sentitweet/data/clusters_create.png'))
