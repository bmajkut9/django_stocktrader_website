from django.contrib import admin
from .models import CashAssets, StockAssets, BuyStockHistory, SellStockHistory
# Register your models here.

admin.site.register(CashAssets)
admin.site.register(StockAssets)
admin.site.register(BuyStockHistory)
admin.site.register(SellStockHistory)

