from django.urls import path
from . import views

urlpatterns = [
    path("investments/", views.investments_view, name = "investments"),
    path('ticker_search/<str:ticker>/', views.ticker_search_view, name='ticker_search'),
]
