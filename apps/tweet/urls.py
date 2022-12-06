from django.urls import path
from tweet.views import hashtag

urlpatterns = [
	path('hashtag/<str:hashtag_value>/', hashtag, name='hashtag'),
]
