from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from stock.models import Company
from stock.utils import (get_company_by_symbol_or_name,
                         get_relevent_model_context)
from tweet.models import HashTag, Set


@login_required(login_url="/login/")
def hashtag(request, hashtag_value):
    companies = Company.objects.all()
    hashtags = HashTag.objects.all().annotate(t_count=Count('tweets')).order_by('-t_count')

    try:
        hashtag = HashTag.objects.get(value=f'#{hashtag_value}')
    except HashTag.ObjectDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    context = get_relevent_model_context()
    context['hashtag'] = hashtag

    return render(request, 'tweet/hashtag_detail.html', context)


@login_required(login_url="/login/")
def set_view(request, id):
    companies = Company.objects.all()
    hashtags = HashTag.objects.all().annotate(t_count=Count('tweets')).order_by('-t_count')

    try:
        set_object = Set.objects.get(pk=id)
    except Set.ObjectDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    context = get_relevent_model_context()
    context['set'] = set_object

    return render(request, 'tweet/set_detail.html', context)