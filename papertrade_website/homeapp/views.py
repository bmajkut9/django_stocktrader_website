import requests
from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    API_KEY = "9K40A1BBDYXSDIM8"
    url = "https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=" + API_KEY
    gainers = []
    losers = []
    
    r = requests.get(url)
    data = r.json()
    gainers_data = data.get('top_gainers', [])
    losers_data = data.get('top_losers', [])
    
    for gainer in gainers_data[:10]:
        gainer_data = []
        gainer_ticker = gainer.get("ticker", "N/A")
        gainer_data.append(gainer_ticker)
        gainer_change_percentage = gainer.get("change_percentage", "N/A")
        gainer_data.append(gainer_change_percentage)
        
        gainers.append(gainer_data)
        
    for loser in losers_data [:10]:
        loser_data = {}
        loser_ticker = loser.get("ticker", "N/A")
        loser_change_percentage = loser.get("change_percentage", "N/A")
        
        loser_data["ticker"] = loser_ticker
        loser_data["change_percentage"] = loser_change_percentage
                
        losers.append(loser_data)
    
    
    
    if request.user.is_authenticated:
        return render(request, "home.html", {"gainers": gainers, "losers": losers})
    else:
        return redirect("login")
