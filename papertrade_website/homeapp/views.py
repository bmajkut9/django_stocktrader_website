import requests
from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    
    gainers_url = "https://financial-modeling-prep.p.rapidapi.com/v3/stock_market/gainers"
    gainers_headers = {
        "X-RapidAPI-Key": "2daf8d998cmsh05df2a294110463p1bc9fbjsnbc6f35ce07c0",
        "X-RapidAPI-Host": "financial-modeling-prep.p.rapidapi.com"
    }
    
    gainers_r = requests.get(gainers_url, headers=gainers_headers)

    losers_url = "https://financial-modeling-prep.p.rapidapi.com/v3/stock_market/losers"
    losers_headers = {
        "X-RapidAPI-Key": "2daf8d998cmsh05df2a294110463p1bc9fbjsnbc6f35ce07c0",
        "X-RapidAPI-Host": "financial-modeling-prep.p.rapidapi.com"
    }
    
    losers_r = requests.get(losers_url, headers=losers_headers)
    
    mostActive_url = "https://financial-modeling-prep.p.rapidapi.com/v3/stock_market/actives"

    mostActive_headers = {
        "X-RapidAPI-Key": "2daf8d998cmsh05df2a294110463p1bc9fbjsnbc6f35ce07c0",
        "X-RapidAPI-Host": "financial-modeling-prep.p.rapidapi.com"
    }

    mostActive_r = requests.get(mostActive_url, headers=mostActive_headers)


    gainers = []
    losers = []
    mostActive = []
    
    
    gainers_data = gainers_r.json()
    losers_data = losers_r.json()
    mostActive_data = mostActive_r.json()
    print("ready")
    
    for gainer in gainers_data[:10]:
        gainer_data = {}
        gainer_ticker = gainer.get("symbol", "N/A")
        gainer_change_percentage = gainer.get("changesPercentage", "N/A")
        
        gainer_data["symbol"] = gainer_ticker
        gainer_data["change_percentage"] = gainer_change_percentage
        
        gainers.append(gainer_data)
    print("gainers:", gainers)
        
    for loser in losers_data[:10]:
        loser_data = {}
        loser_ticker = loser.get("symbol", "N/A")
        loser_change_percentage = loser.get("changesPercentage", "N/A")
        
        loser_data["symbol"] = loser_ticker
        loser_data["change_percentage"] = loser_change_percentage
                
        losers.append(loser_data)
    print("losers", losers)

    for active in mostActive_data[:10]:
        active_data = {}
        active_ticker = active.get("symbol", "N/A")
        active_change_percentage = active.get("changesPercentage", "N/A")
        
        active_data["symbol"] = active_ticker
        active_data["change_percentage"] = active_change_percentage
        
        mostActive.append(active_data)
    print("mostActive:", mostActive)
    
    
    """print("API Response Status Code:", gainers_r.status_code, losers_r.status_code, mostActive_r.status_code)"""
    
    if request.user.is_authenticated:
        return render(request, "home.html", {"gainers": gainers, "losers": losers, "mostActive": mostActive})
    else:
        return redirect("login")
