from django.shortcuts import render, redirect

from tweet.models import Tweet
from core.models import Company

def index(request):
    tweet = Tweet.objects.first()
    companies = Company.objects.all()

    context = {'tweet': tweet, 'companies': companies}

    return render(request, 'core/index.html', context)

def detail(request, symbol):
    companies = Company.objects.filter(symbol=symbol)

    if not companies.exists():
        return redirect('/')

    company = companies.first()
    tweets = company.tweets.all()[:50]

    context = {'company': company, 'tweets': tweets}
    return render(request, 'core/detail.html', context)