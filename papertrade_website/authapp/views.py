from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def login(request):
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/home/")
        else:
            return render(request, "signup.html", {"form": form})
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})
