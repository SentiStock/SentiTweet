from django.conf import settings
from django.core.management.base import BaseCommand
from tweet.models import Tweet
from tweet.utils import (create_clusters, get_top_keywords, get_vectorizer,
                         plot_clusters)


class Command(BaseCommand):

    help = "Create clusters and print common words"

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='Number of clusters to try')

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Creating clusters...'))

        number_of_clusters = options['number']

        tweets = Tweet.as_dataframe()
        print(f'Creating clusters for {len(tweets)} tweets')

        # TODO do we want to drop duplicates on cleaned text?
        tfidf = get_vectorizer()
        tfidf.fit(tweets.cleaned_text)
        text = tfidf.transform(tweets.cleaned_text)

        clusters = create_clusters(text, number_of_clusters)

        plot_clusters(text, clusters)

        print('Top key words for all the clusters are:')
        get_top_keywords(text, clusters, tfidf.get_feature_names(), 10)
        # except Exception as e:
        #     self.stdout.write(f'Something went wrong: {e}')

        self.stdout.write(self.style.SUCCESS(
            'Successfully created clusters, saved as: sentitweet/data/clusters_create.png'))
