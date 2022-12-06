from django.urls import path
from tweet.views import hashtag, set_view

urlpatterns = [
	path('hashtags/<str:hashtag_value>/', hashtag, name='hashtag'),
	path('sets/<str:id>/', set_view, name='set'),
]
