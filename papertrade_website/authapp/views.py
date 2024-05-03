from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout


# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect("/home/")
            else:
                return render(request, "login.html", {"error_message": "Account deleted"})
            
        else:
            return render(request, "login.html", 
                          {"username": username, 
                          "password": password, 
                          "error_message": "Email or password is incorrect"})
        
    else:
        return render(request, "login.html")
    

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect("/home/")
        else:
            return render(request, "signup.html", {"form": form})
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

def logout_view(request):
    logout(request)
    return render(request, "logout.html")
