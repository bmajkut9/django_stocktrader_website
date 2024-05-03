from django.urls import path
from . import views

urlpatterns = [
    path("todos/", views.todos, name = "Todos"),
    path("about/", views.about, name = "About"),
    path("contact/", views.contact, name = "Contact"),
]