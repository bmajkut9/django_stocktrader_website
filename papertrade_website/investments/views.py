from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def ticker_search_view(request, ticker):
        return HttpResponse(f"Ticker entered: {ticker}")
    

def investments_view(request):
    if request.method == "POST":
        ticker = request.POST.get("ticker")
        return redirect("ticker_search", ticker=ticker)
    
    return render(request, "investments.html")

