from django.db.models import Count, Q
from stock.models import Company
from tweet.models import HashTag, Set, TwitterUser
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


def get_relevent_model_context():
    companies = Company.objects.all().annotate(t_count=Count('tweets')).order_by('-t_count')
    hashtags = HashTag.objects.all().annotate(t_count=Count('tweets')).order_by('-t_count')
    users = TwitterUser.objects.all().annotate(t_count=Count('tweets')).order_by('-t_count')
    sets = Set.objects.filter(mode='public')#.order_by('followers')

    return {'sets': sets, 'companies': companies, 'hashtags': hashtags, 'users': users}


def get_cluster_context(tweets):
    if len(tweets) > 50:
        best_tweets, top_words = cluster_tweets(tweets, number_of_best_tweets=5)
        # TODO make best_tweets to be all attributes
        return list(zip(top_words.values(), best_tweets.groupby('cluster').text.apply(list)))
    return None

