from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from stock.models import Company
from stock.utils import get_company_by_symbol_or_name
from tweet.models import HashTag


def hashtag(request, hashtag_value):
    companies = Company.objects.all()
    hashtags = HashTag.objects.all().annotate(t_count=Count('tweets')).order_by('-t_count')

    hashtag = HashTag.objects.get(value=f'#{hashtag_value}')
    try:
        pass
    except HashTag.ObjectDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    context = {'hashtag': hashtag, 'companies': companies, 'hashtags': hashtags}
    return render(request, 'tweet/hashtag_detail.html', context)