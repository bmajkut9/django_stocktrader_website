from django.shortcuts import render, HttpResponse
from .models import TodoItem
# Create your views here.

def login(request):
    return render(request, "login.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})
