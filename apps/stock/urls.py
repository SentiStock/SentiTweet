from django.urls import path
from stock.views import company

urlpatterns = [
	path('<str:company_symbol_or_name>/', company, name='comapny'),
]
