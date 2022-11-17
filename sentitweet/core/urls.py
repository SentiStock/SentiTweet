from django.urls import path

from . import views

urlpatterns = [
    path('<str:symbol>/', views.detail, name='detail'),
    path('', views.index, name='index'),
]