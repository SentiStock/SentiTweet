from django.db.models import Q
from stock.models import Company


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