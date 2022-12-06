from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('company/', include('stock.urls')),
    path('tweet/', include('tweet.urls')),

    path('', include("authentication.urls")), 
    path('', include("home.urls"))
]
