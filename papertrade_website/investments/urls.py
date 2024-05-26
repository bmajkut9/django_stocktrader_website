from django.urls import path
from . import views

urlpatterns = [
    path("investments/", views.investments_view, name = "Investments"),
]