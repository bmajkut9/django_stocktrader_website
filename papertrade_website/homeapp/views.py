import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    """
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
    """
    mostActive_url = "https://financial-modeling-prep.p.rapidapi.com/v3/stock_market/actives"

    mostActive_headers = {
        "X-RapidAPI-Key": "2daf8d998cmsh05df2a294110463p1bc9fbjsnbc6f35ce07c0",
        "X-RapidAPI-Host": "financial-modeling-prep.p.rapidapi.com"
    }

    mostActive_r = requests.get(mostActive_url, headers=mostActive_headers)


    gainers = []
    losers = []
    mostActive = []
    
    
    mostActive_data = mostActive_r.json()
    """
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
    """
    for active in mostActive_data[:10]:
        active_data = {}
        active_ticker = active.get("symbol", "N/A")
        active_change_percentage = active.get("changesPercentage", "N/A")
        
        active_data["symbol"] = active_ticker
        active_data["change_percentage"] = active_change_percentage
        
        mostActive.append(active_data)

        
    news_url = "https://finance.yahoo.com/"
    news_html = requests.get(news_url)
    
    articles = []
    
    news_s = BeautifulSoup(news_html.content, "html.parser")
    news_results = news_s.find_all(attrs={"data-testid": "storyitem"})
    
    for result in news_results[:3]:
        current_article = {}
        
        news_info = result.find("a")
        news_img_tag = result.find("img")
        
        if news_info:
            news_title = news_info.get("title")
            current_article["title"] = news_title
            
            news_link = news_info.get("href")
            current_article["link"] = news_link
            
            news_image = news_img_tag.get("src")
            current_article["image"] = news_image
            
            articles.append(current_article)
    
    print("All articles", articles)
            
    
    

    if request.user.is_authenticated:
        return render(request, "home.html", {"gainers": gainers, "losers": losers, "mostActive": mostActive, "articles": articles})
    else:
        return redirect("login")
