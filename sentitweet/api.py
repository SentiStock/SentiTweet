import json

from authentication.models import Contributor, Favorite
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Count, Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from stock.models import Company
from tweet.models import HashTag, Set, TwitterUser

from sentitweet.serializers import (CompanySerializer, HashTagSerializer,
                                    SetSerializer, TwitterUserSerializer)


@api_view(['GET'])
@login_required
def search_all_objects(request):
    try:
        request_objects = request.GET['objects']
        query = request.GET['query']
    except Exception as e:
        return JsonResponse({'error': 'please provide a search query and the objects seperated by ,'})

    try:
        final = {}
        for request_object in request_objects.split(','):
            request_object = request_object.lower()
            if request_object.lower() == 'company':
                companies = Company.objects.filter(Q(name__icontains=query) | Q(symbol__icontains=query)).annotate(t_count=Count('tweets')).order_by('-t_count')[:50]
                final['companies'] = CompanySerializer(companies, many=True).data
            elif request_object.lower() == 'set':
                sets = Set.objects.filter(Q(name__icontains=query) & (Q(mode='public') | Q(creator=request.user)))[:50]
                final['sets'] = SetSerializer(sets, many=True).data
            elif request_object.lower() == 'hashtag':
                hashtags = HashTag.objects.filter(value__icontains=query).annotate(t_count=Count('tweets')).order_by('-t_count')[:50]
                final['hashtags'] = HashTagSerializer(hashtags, many=True).data
            elif request_object.lower() == 'twitteruser':
                twitter_users = TwitterUser.objects.filter(username__icontains=query).annotate(t_count=Count('tweets')).order_by('-t_count')[:50]
                final['twitterusers'] = TwitterUserSerializer(twitter_users, many=True).data
    except Exception as e:
        JsonResponse({'error': 'Something went wrong'})

    return JsonResponse({'data': final})


# @login_required
@api_view(['POST'])
def toggle_favorite(request):
    try:
        request_object_type = request.data['object_type'].lower()
        request_object_id = request.data['object_id']
    except Exception as e:
        return JsonResponse({'error': 'please provide the object type and the object id'})

    user = request.user
    message = ''

    try:
        if request_object_type == 'company':
            object_to_toggle = Company.objects.get(id=request_object_id)
        elif request_object_type == 'set':
            object_to_toggle = Set.objects.get(id=request_object_id)
        elif request_object_type == 'hashtag':
            object_to_toggle = HashTag.objects.get(id=request_object_id)
        elif request_object_type == 'twitteruser':
            object_to_toggle = TwitterUser.objects.get(id=request_object_id)
        elif request_object_type == 'contributor':
            object_to_toggle = Contributor.objects.get(id=request_object_id)

        try:
            favorite_exists = Favorite.objects.get(
                favorite_id=request_object_id, 
                favorite_ct__model=request_object_type
            )
            favorite_exists.delete()
            message = 'unfavorited'
        except: # The object is not yet a favorite
            Favorite.objects.create(favorite=object_to_toggle, user=user)
            message = 'favorited'

    except Exception as e:
        print(e)
        JsonResponse({'error': f'Something went wrong {e}'})

    return JsonResponse({'success': message})
