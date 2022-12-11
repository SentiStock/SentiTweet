from django.urls import path
from stock.views import company, company_detail, discover, trends

urlpatterns = [

    path('discover', discover, name='discover'),
	path('trends', trends, name='trends'),
	path('companies/', company, name='comapny'),
	path('companies/<str:company_symbol_or_name>/', company_detail, name='comapany_detail'),
]

