# from sentitweet import plotly_app
# from tweet.graphs import *
# import tweet.graphs.hashtag_detail
from django.contrib import admin
from django.urls import include, path
# from stock.graphs import *
from tweet.graphs import *

from sentitweet.api import search_all_objects, toggle_favorite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/search/', search_all_objects),
    path('api/favorite/', toggle_favorite),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

    path('', include('stock.urls')),
    path('', include('tweet.urls')),

    path('', include("authentication.urls")), 
    path('', include("home.urls"))
]
