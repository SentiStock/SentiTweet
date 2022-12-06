from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from stock.models import Company
from stock.utils import get_company_by_symbol_or_name
from tweet.models import HashTag


def company(request, company_symbol_or_name):
    companies = Company.objects.all()
    hashtags = HashTag.objects.all().annotate(t_count=Count('tweets')).order_by('-t_count')

    company = get_company_by_symbol_or_name(company_symbol_or_name)
    
    if not company:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render({}, request))
    try:
        pass
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    context = {'company': company, 'companies': companies, 'hashtags': hashtags}
    return render(request, 'stock/detail.html', context)