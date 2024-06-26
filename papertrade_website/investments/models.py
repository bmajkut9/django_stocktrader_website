from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# cash to buy stocks with
class CashAssets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cash_amount = models.DecimalField(max_digits=99, decimal_places=2, default=0)
    total_cash_withdrawn = models.DecimalField(max_digits=99, decimal_places=2, default=0)
    
# each ticker and ammount of stocks for that ticker
class StockAssets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_value_amount = models.DecimalField(max_digits=999, decimal_places=2)
    stock_count = models.DecimalField(max_digits=99, decimal_places=2, default=0)
    ticker = models.CharField(max_length=10, default="----")

# the stock ticker and the ammount of stocks, adds to StockAssets
class BuyStockHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buy_date = models.DateField(auto_now_add=True)
    stock_purchased_count = models.DecimalField(max_digits=99, decimal_places=2, default=0)
    stock_value_amount = models.DecimalField(max_digits=999, decimal_places=2, default=0)
    ticker = models.CharField(max_length=10, default="----")
    
class SellStockHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sell_date = models.DateField(auto_now_add=True)
    stock_sold_count = models.DecimalField(max_digits=99, decimal_places=2, default=0)
    stock_value_amount = models.DecimalField(max_digits=999, decimal_places=2, default=0)
    ticker = models.CharField(max_length=10, default="----")
    


    


    

    
