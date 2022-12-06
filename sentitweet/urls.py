from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('stock.urls')),
    path('', include('tweet.urls')),

    path('', include("authentication.urls")), 
    path('', include("home.urls"))
]
