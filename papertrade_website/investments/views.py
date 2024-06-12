from .forms import AddCashForm, BuyForm, SellForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import DatabaseError
import datetime as datetime
import json
from django.db.models.functions import Coalesce
from .models import CashAssets, BuyStockHistory, SellStockHistory, StockAssets
from django.db.models import Sum, F, Value as V, DecimalField
import yfinance as yf
from decimal import Decimal, ROUND_HALF_UP

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


def ticker_search_view(request, ticker=None):
    if request.method == 'POST':
        stock_amount = request.POST.get('stock_amount')
        action = request.POST.get('action')

        if action == 'buy':
            form = BuyForm(request.POST)
            if form.is_valid():
                stock_amount = form.cleaned_data['stock_amount']
                price = yf.Ticker(ticker).info.get("currentPrice")
                ticker = yf.Ticker(ticker).info.get("symbol")
                if price is not None:
                    price_decimal = Decimal(price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    
                BuyStockHistory.objects.create(
                    user=request.user, 
                    stock_purchased_count=stock_amount, 
                    stock_value_amount=price_decimal, 
                    ticker=ticker
                    )
                
                return redirect('investments')
            
     
        elif action == 'sell':
            form = SellForm(request.POST)
            if form.is_valid():
                stock_amount = form.cleaned_data['stock_amount']
        
    else:
        buy_form = BuyForm()
        sell_form = SellForm()
        
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period='max')



    dates = hist.index.to_pydatetime()
    filtered_dates = []
    filtered_values = []
    year_labels = []

    for i, date in enumerate(dates):
        if i == 0 or (date.month != dates[i - 1].month or date.year != dates[i - 1].year):
            filtered_dates.append(date.strftime('%Y-%m-%d'))
            filtered_values.append(hist['Close'].iloc[i])
            # Add year label only for the first month of the year
            if date.month == 1:
                year_labels.append(date.strftime('%Y'))
            else:
                year_labels.append('')

    chartData = {
        'dates': filtered_dates,
        'values': filtered_values,
        'year_labels': year_labels,
    }
    
    
    
    three_month_hist = stock.history(period='3mo')
    three_month_dates = three_month_hist.index.to_pydatetime()

    three_month_filtered_dates = []
    three_month_filtered_values = []
    three_month_week_labels = []

    current_week = None

    for i, date in enumerate(three_month_dates):
        three_month_filtered_dates.append(date.strftime('%Y-%m-%d'))
        three_month_filtered_values.append(three_month_hist['Close'].iloc[i])
        
        # Get the ISO week number
        week_number = date.isocalendar()[1]
        
        # Check if it's the first trading day of a new week
        if week_number != current_week:
            three_month_week_labels.append(date.strftime('%m/%d'))
            current_week = week_number
        else:
            three_month_week_labels.append('')


    # Prepare chart data
    three_month_chartData = {
        'dates': three_month_filtered_dates,
        'values': three_month_filtered_values,
        'week_labels': three_month_week_labels,
    }
    
    print("weeklabels: ", three_month_chartData['week_labels'])
    
    
    importantData = {
        "name": info.get("shortName"),
        "ticker": info.get("symbol"),
        "industry": info.get("industryDisp"),
        "sector": info.get("sectorDisp"),
        "longDescription": info.get("longBusinessSummary"),
        "currentPrice": info.get("currentPrice"),
        "marketCap": info.get("marketCap"),
        "trailingPE": info.get("trailingPE"),
        "forwardPE": info.get("forwardPE"),
        "trailingEps": info.get("trailingEps"),
        "dividendYield": info.get("dividendYield"),
        "beta": info.get("beta"),
        "totalRevenue": info.get("totalRevenue"),
        "grossMargins": info.get("grossMargins"),
        "operatingMargins": info.get("operatingMargins"),
        "profitMargins": info.get("profitMargins"),
        "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow")
    }
    return render(request, "ticker_search.html", {"ticker": ticker, "importantData": importantData, "chartData": json.dumps(chartData), "three_month_chartData": json.dumps(three_month_chartData) })


def investments_view(request):    
    if request.method == "POST":
        if 'search_ticker' in request.POST:
            ticker = request.POST.get("search_ticker")
            print("ticker is", ticker)
            return redirect("ticker_search", ticker=ticker)
         
        elif 'add_cash' in request.POST:
            add_cash_form = AddCashForm(request.POST)
            if add_cash_form.is_valid():
                amount = add_cash_form.cleaned_data['add_cash']
                print("the amount is", amount)
                add_cash(request.user, amount)
                return redirect('investments')
            else:
                print("not valid")
                print("Form errors:", add_cash_form.errors)
                print(add_cash_form)
            
            
            
    cash_amount, total_spent, total_cash_withdrawn, stock_assets_value,stock_bought_value, stock_sold_value, net_profit_loss, net_percent = get_cash_stats(request.user)
    
    user = request.user 
    stock_assets = StockAssets.objects.filter(user=user)
    
    investments_display_data = []
    
    for asset in stock_assets:
        total_value = asset.stock_value_amount * asset.stock_count
        investments_display_data.append({
            'ticker': asset.ticker,
            'price': asset.stock_value_amount,
            'total_value': total_value,
            #'daily_change_percentage': yfiancecode
        })
        
    print("investments display data:", investments_display_data)
        
    
    
    
    context = {
        "cash_amount": cash_amount,
        "total_spent": total_spent, 
        "total_cash_withdrawn": total_cash_withdrawn,
        "stock_assets_value": stock_assets_value,
        "stock_bought_value": stock_bought_value,
        "stock_sold_value": stock_sold_value, 
        "net_profit_loss": net_profit_loss,
        "net_percent": net_percent,
        "investments_display_data": investments_display_data
        }
    
    return render(request, "investments.html", context)

