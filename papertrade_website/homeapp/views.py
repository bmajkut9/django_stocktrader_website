import requests
import json
from django.utils.safestring import mark_safe
from datetime import timedelta
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from investments.models import BuyStockHistory, SellStockHistory, StockAssets

# Create your views here.

def get_date_range(user): # arg = request.user
    buy_dates = BuyStockHistory.objects.filter(user=user).values_list("buy_date", flat=True)
    sell_dates = SellStockHistory.objects.filter(user=user).values_list("sell_date", flat=True)
    all_dates = list(buy_dates) + list(sell_dates)
    
    if all_dates:
        min_date = min(all_dates)
        max_date = max(all_dates)
        date_diff = (max_date - min_date).days
                
        if date_diff <= 7:
            unit_type = "day"
        elif date_diff <= 31:
            unit_type = "week"
        else:
            unit_type = "month"
        return min_date, max_date, unit_type
    
    else:
        return None, None, None

# gets each date where something happened and gives the overall ending value for that date
def aggregate_stock_values(user):
    data = {}

    buy_data = BuyStockHistory.objects.filter(user=user).values("buy_date").annotate(total_value=Sum(F("stock_value_amount") * F("stock_purchased_count")))
    sell_data = SellStockHistory.objects.filter(user=user).values("sell_date").annotate(total_value=Sum(F("stock_value_amount") * F("stock_sold_count")))
    
    for entry in buy_data:
        date = entry["buy_date"]
        if date in data:
            data[date] += entry["total_value"]
        else:
            data[date] = entry["total_value"]
        
    for entry in sell_data:
        date = entry["sell_date"]
        if date in data:
            data[date] -= entry["total_value"] 
        else:
            data[date] = -entry["total_value"]
    
    sorted_data = dict(sorted(data.items()))
    return sorted_data 
            

def home(request):
    chart_dates_config = {}
    chart_dates_config["min_date"], chart_dates_config["max_date"], chart_dates_config["unit_type"] = get_date_range(request.user)
    
    stock_values = aggregate_stock_values(request.user)
    dates = list(stock_values.keys())
    formatted_dates = []
    cumulative_values = []
    cumulative_value = 0
    
    for date in dates:
        formatted_dates.append(date.strftime("%m/%d/%Y"))
        cumulative_value += stock_values[date] 
        cumulative_values.append(float(cumulative_value))
        
    chart_data = {"dates": formatted_dates, "cumulative_values": cumulative_values}
    
    chart_data_json = json.dumps(chart_data)
    print("chart data json", chart_data_json)
    
    chart_data_json_safe = mark_safe(chart_data_json)
    print("chart data safe", chart_data_json_safe)
    
    
    
    
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
    
    investment_assets = {}
    # for total investments text display
    total_investment_result = StockAssets.objects.filter(user = request.user).aggregate(total_investment=Sum(F("stock_value_amount") * F("stock_count")) * 100 / 100)
    total_investment_value = total_investment_result['total_investment'] or 0
    investment_assets["total"] = total_investment_value
    
    if chart_data["cumulative_values"]:
        if len(chart_data["cumulative_values"]) >= 2:
            list_length = len(chart_data["cumulative_values"])
            full_change_percentage = (chart_data["cumulative_values"][list_length - 1] - chart_data["cumulative_values"][list_length - 2]) / chart_data["cumulative_values"][list_length - 2] * 100
            change_percentage_int = int(full_change_percentage * 100)
            investment_assets["change_percentage"] = change_percentage_int / 100 
            print(chart_data["cumulative_values"][list_length - 1], chart_data["cumulative_values"][list_length - 2])
    else:
        investment_assets["change_percentage"] = 0
        
    print(chart_data)
    print(chart_dates_config)
    if request.user.is_authenticated:
        return render(request, "home.html", {
            "chart_dates_config": chart_dates_config, 
            "chart_data": chart_data_json_safe, 
            "investment_assets": investment_assets, 
            "gainers": gainers, 
            "losers": losers, 
            "mostActive": mostActive, 
            "articles": articles})
    else:
        return redirect("login")
