from django.urls import path
from tweet.views import (hashtag, hashtag_detail, set_create, set_detail_view,
                         set_view, user, user_detail)

urlpatterns = [
	path('hashtags/', hashtag, name='hashtag'),
	path('hashtags/<str:hashtag_value>/', hashtag_detail, name='hashtag_detail'),
	path('sets/', set_view, name='set'),
	path('sets/create/', set_create, name='set_create'),
	path('sets/<str:id>/', set_detail_view, name='set_detail'),
	path('users/', user, name='user'),
	path('users/<str:id>/', user_detail, name='user_detail'),
]
