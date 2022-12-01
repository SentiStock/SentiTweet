from django.conf import settings
from django.core.management.base import BaseCommand
from tweet.models import Tweet
from tweet.utils import find_optimal_clusters_sse, get_vectorizer


class Command(BaseCommand):

    help = "Find best number of clusters"

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number', type=int, help='Up to number of clusters to try')

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(
            'Creating clusters...'))

        max_k=20
        if options['number']:
            max_k=options['number']

        tweets = Tweet.as_dataframe()
        print(f'Creating clusters for {len(tweets)} tweets')

        # TODO do we want to drop duplicates on cleaned text?
        tfidf = get_vectorizer()
        tfidf.fit(tweets.cleaned_text)
        text = tfidf.transform(tweets.cleaned_text)

        find_optimal_clusters_sse(text, max_k=max_k)

        # except Exception as e:
        #     self.stdout.write(f'Something went wrong: {e}')

        self.stdout.write(self.style.SUCCESS(
            'Successfully created clusters, saved as: sentitweet/data/clusters_find.png'))
