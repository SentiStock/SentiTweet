from django.db.models import Count, Q
from stock.models import Company
from tweet.models import Contributor, HashTag, Set, TwitterUser
from tweet.utils import cluster_tweets


def get_company_by_symbol_or_name(symbol_or_name):
    companies = Company.objects.all()

    if len(companies.filter(symbol=symbol_or_name)) == 1:
        return companies.get(symbol=symbol_or_name)
    if len(companies.filter(name=symbol_or_name)) == 1:
        return companies.get(name=symbol_or_name)

    company_filter = companies.filter(
        Q(name__istartswith=symbol_or_name)
        | Q(symbol__istartswith=symbol_or_name)
    )
    if company_filter.exists():
        return company_filter.first()

    return None


def get_relevant_model_context(companies=False, hashtags=False, sets=False, users=False, contributors=False):

    companies_objects = Company.objects.all().annotate(t_count=Count('tweets')).order_by('-t_count') if companies else dict()
    hashtags_objects = HashTag.objects.all().annotate(t_count=Count('tweets')).order_by('-t_count') if hashtags else dict()
    users_objects = TwitterUser.objects.all().annotate(t_count=Count('tweets')).order_by('-t_count') if users else dict()
    sets_objects = Set.objects.filter(mode='public') if sets else dict()
    contributors_objects = Contributor.objects.all() if contributors else dict()

    return {
        'sets': sets_objects, 
        'companies': companies_objects,
        'hashtags': hashtags_objects,
        'users': users_objects,
        'contributors': contributors_objects
    }


def get_cluster_context(tweets):
    if len(tweets) > 50:
        best_tweets, top_words = cluster_tweets(tweets, number_of_best_tweets=5)
        # TODO make best_tweets to be all attributes
        return zip(top_words.values(), best_tweets.groupby('cluster').text.apply(list))
    return None

