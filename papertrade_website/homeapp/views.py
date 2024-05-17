import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.db.models import Sum
from investments.models import BuyStockHistory

# Create your views here.

def home(request):
    gainers = []
    losers = []
    mostActive = []

        
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
            
    
    investment_assets = BuyStockHistory.objects.filter(user = request.user).aggregate(total_investment=Sum('stock_value_amount'))['total_investment']
    if not investment_assets:
        investment_assets = 0
        

    if request.user.is_authenticated:
        return render(request, "home.html", {"investment_assets": investment_assets, "gainers": gainers, "losers": losers, "mostActive": mostActive, "articles": articles})
    else:
        return redirect("login")
