from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('search/', views.SearchView.as_view(), name='search_page'),
    path('clear-search-history', views.ClearSearchHistoryView.as_view(), name='clear_search_page'),
]