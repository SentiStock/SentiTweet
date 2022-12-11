from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from stock.models import Company
from stock.utils import (get_cluster_context, get_company_by_symbol_or_name,
                         get_relevent_model_context)
from tweet.models import HashTag
from tweet.utils import cluster_tweets


@login_required(login_url="/login/")
def company(request):
    try:
        pass
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    context = get_relevent_model_context()

    return render(request, 'stock/companies.html', context)


@login_required(login_url="/login/")
def company_detail(request, company_symbol_or_name):
    company = get_company_by_symbol_or_name(company_symbol_or_name)

    if not company:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render({}, request))
    try:
        pass
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    tweets = company.tweets.all()

    context = get_relevent_model_context()
    context['company'] = company
    context['tweets'] = tweets
    context['clusters'] = get_cluster_context(tweets)

    return render(request, 'stock/company_page.html', context)


@login_required(login_url="/login/")
def discover(request):
    #context = get_relevent_model_context()
    context = {}
    html_template = loader.get_template('stock/discover.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def trends(request):
    #context = get_relevent_model_context()
    context = {}
    html_template = loader.get_template('stock/trends.html')
    return HttpResponse(html_template.render(context, request))