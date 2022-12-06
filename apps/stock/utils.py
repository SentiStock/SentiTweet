from django.db.models import Count, Q
from stock.models import Company
from tweet.models import HashTag, Set


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
    sets = Set.objects.all()#.order_by('followers')

    return {'sets': sets, 'companies': companies, 'hashtags': hashtags}

