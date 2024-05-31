from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import DatabaseError
from django.db.models.functions import Coalesce
from .models import CashAssets, BuyStockHistory, SellStockHistory, StockAssets
from django.db.models import Sum, F, Value as V, DecimalField
import yfinance as yf

def add_cash(user, amount):
    # +amount if adding and -amount if subtracting
    try:
        cash_assets, created = CashAssets.objects.get_or_create(user=user, defaults={'cash_amount': 0, 'total_cash_withdrawn': 0})
    except DatabaseError as e:
        print("Database error", e)
    
    cash_assets.cash_amount += amount
    cash_assets.total_cash_withdrawn += amount
    cash_assets.save()

    
        
def get_cash_stats(user):
    try:
        cash_assets, created = CashAssets.objects.get_or_create(user=user, defaults={'cash_amount': 0, 'total_cash_withdrawn': 0})
    except DatabaseError as e:
        print("Database error", e)
        
    print("cash assets", cash_assets)
        
    cash_amount = cash_assets.cash_amount if cash_assets else 0
    print("cash amount" , cash_amount)
    total_cash_withdrawn = cash_assets.total_cash_withdrawn if cash_assets else 0
    print("total cash withdrawn", total_cash_withdrawn)
    total_spent = total_cash_withdrawn - cash_amount
    
    stock_bought_data = BuyStockHistory.objects.filter(user=user).aggregate(
        total_stock_bought_value=Sum(F('stock_value_amount') * F('stock_purchased_count'))
    )
    unformatted_stock_bought_value = stock_bought_data['total_stock_bought_value'] if stock_bought_data else 0
    stock_bought_value = f"{unformatted_stock_bought_value:.2f}" 
    
    stock_sold_data = SellStockHistory.objects.filter(user=user).aggregate(
        total_stock_sold_value=Sum(F('stock_value_amount') * F('stock_sold_count'))
    )
    unformatted_stock_sold_value = stock_sold_data['total_stock_sold_value'] if stock_sold_data else 0
    stock_sold_value = f"{unformatted_stock_sold_value:.2f}" 

    
    stock_assets_data = StockAssets.objects.filter(user = user).aggregate(total_investment=Coalesce(Sum(F("stock_value_amount") * F("stock_count")), V(0, output_field=DecimalField(decimal_places=2))))
    unformatted_stock_assets_value = stock_assets_data['total_investment']
    stock_assets_value = f"{unformatted_stock_assets_value:.2f}" 

    
    unformatted_net_profit_loss = (cash_amount + unformatted_stock_assets_value) - total_cash_withdrawn
    net_profit_loss = f"{unformatted_net_profit_loss:.2f}"
    unformatted_net_percent = unformatted_net_profit_loss / total_cash_withdrawn * 100
    net_percent = f"{unformatted_net_percent:.2f}"
    
    
    
    return cash_amount, total_spent, total_cash_withdrawn, stock_assets_value, stock_bought_value, stock_sold_value, net_profit_loss, net_percent

# Create your views here.


def ticker_search_view(request, ticker):
        #return HttpResponse(f"Ticker entered: {ticker}")
    return render(request, "ticker_search.html", {"ticker": ticker})


def investments_view(request):
    if request.method == "POST":
        ticker = request.POST.get("ticker")
        return redirect("ticker_search", ticker=ticker)
    
    cash_amount, total_spent, total_cash_withdrawn, stock_assets_value,stock_bought_value, stock_sold_value, net_profit_loss, net_percent = get_cash_stats(request.user)
    
    context = {
        "cash_amount": cash_amount,
        "total_spent": total_spent, 
        "total_cash_withdrawn": total_cash_withdrawn,
        "stock_assets_value": stock_assets_value,
        "stock_bought_value": stock_bought_value,
        "stock_sold_value": stock_sold_value, 
        "net_profit_loss": net_profit_loss,
        "net_percent": net_percent,
        }
    
    return render(request, "investments.html", context)

