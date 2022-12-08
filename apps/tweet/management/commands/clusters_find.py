from django.conf import settings
from django.core.management.base import BaseCommand
from tweet.models import Tweet
from tweet.utils import (find_optimal_clusters_silh_score,
                         find_optimal_clusters_sse, get_vectorizer)


class Command(BaseCommand):

    help = "Find best number of clusters"

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='Up to number of clusters to try')

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(
            'Creating clusters...'))

        max_k=20
        if options['number']:
            max_k=options['number']

        tweets = Tweet.as_dataframe()
        tweets.drop_duplicates(subset=["cleaned_text"], inplace=True)
        tweets.reset_index(inplace=True, drop=True)
        print(f'Creating clusters for {len(tweets)} tweets')

        tfidf = get_vectorizer()
        tfidf.fit(tweets.cleaned_text)
        text = tfidf.transform(tweets.cleaned_text)

        # find_optimal_clusters_sse(text, max_k=max_k)
        print(find_optimal_clusters_silh_score(text, max_k))

        self.stdout.write(self.style.SUCCESS(
            'Successfully created clusters, saved as: sentitweet/data/clusters_find.png'))
