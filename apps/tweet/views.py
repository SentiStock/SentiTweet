from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from stock.models import Company
from stock.utils import (get_cluster_context, get_company_by_symbol_or_name,
                         get_relevent_model_context)
from tweet.forms import SetForm
from tweet.models import HashTag, Set, TwitterUser


@login_required(login_url="/login/")
def hashtag(request):
    try:
        pass
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    context = get_relevent_model_context()

    return render(request, 'tweet/hashtags.html', context)


@login_required(login_url="/login/")
def hashtag_detail(request, hashtag_value):
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

    tweets = hashtag.tweets.all()

    context = get_relevent_model_context()
    context['hashtag'] = hashtag
    context['tweets'] = tweets
    context['clusters'] = get_cluster_context(tweets)

    return render(request, 'tweet/hashtag_company_page.html', context)


@login_required(login_url="/login/")
def set_view(request):
    try:
        pass
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    context = get_relevent_model_context()

    return render(request, 'tweet/sets.html', context)


@login_required(login_url="/login/")
def set_detail_view(request, id):
    try:
        set_object = Set.objects.get(pk=id)
    except Set.ObjectDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    tweets = set_object.tweets.all()

    context = get_relevent_model_context()
    context['set'] = set_object
    context['tweets'] = tweets
    context['clusters'] = get_cluster_context(tweets)

    return render(request, 'tweet/set_company_page.html', context)

@login_required(login_url="/login/")
def set_create(request): 
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            set_object = form.save(commit=False)
            set_object.creator = request.user
            # set_object.mode = request.POST.get('mode')
            set_object.save()
            form.save_m2m()
            return redirect('set_detail', set_object.id)
    else:
        form = SetForm()
 
    context = get_relevent_model_context()
    context['form']= form
    return render(request, 'tweet/set_create.html', context)


@login_required(login_url="/login/")
def user(request):
    try:
        pass
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    context = get_relevent_model_context()

    return render(request, 'tweet/users.html', context)


@login_required(login_url="/login/")
def user_detail(request, id):
    try:
        user = TwitterUser.objects.get(pk=id)
    except Set.ObjectDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

    tweets = user.tweets.all()

    context = get_relevent_model_context()
    context['user'] = user
    context['tweets'] = tweets
    context['clusters'] = get_cluster_context(tweets)

    return render(request, 'tweet/user_company_page.html', context)