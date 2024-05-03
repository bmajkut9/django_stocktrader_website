from django.shortcuts import render, redirect, HttpResponse
from .models import TodoItem


# Create your views here.

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})

def about(request):
    if request.user.is_authenticated:
        return render(request, "about.html")
    else:
        return redirect("login")

def contact(request):
    if request.user.is_authenticated:
        return render(request, "contact.html")
    else:
        return redirect("login")
