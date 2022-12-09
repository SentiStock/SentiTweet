# from sentitweet import plotly_app
# from tweet.graphs import *
# import tweet.graphs.hashtag_detail
from django.contrib import admin
from django.urls import include, path
# from stock.graphs import *
from tweet.graphs import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

    path('', include('stock.urls')),
    path('', include('tweet.urls')),

    path('', include("authentication.urls")), 
    path('', include("home.urls"))
]
