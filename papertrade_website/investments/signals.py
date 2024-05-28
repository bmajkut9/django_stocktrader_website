from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import BuyStockHistory, StockAssets, CashAssets, SellStockHistory


@receiver(post_save, sender=User)
def create_cash_assets(sender, instance, created, **kwargs):
    if created:
        CashAssets.objects.create(user=instance)


@receiver(post_save, sender=BuyStockHistory)
@receiver(post_save, sender=SellStockHistory)
def update_stock_assets(sender, instance, created, **kwargs):
    if created:
        if sender == BuyStockHistory:
            total_cost = instance.stock_value_amount * instance.stock_purchased_count 
            cash_assets = CashAssets.objects.get(user = instance.user)
            cash_assets.cash_amount -= total_cost
            cash_assets.save()
            
            stock_asset, new_entry = StockAssets.objects.get_or_create(
                user = instance.user,
                ticker = instance.ticker,
                defaults = {
                    'stock_value_amount': instance.stock_value_amount,
                    'stock_count': instance.stock_purchased_count
                }
            )
            if not new_entry:
                stock_asset.stock_value_amount += instance.stock_value_amount
                stock_asset.stock_count += instance.stock_purchased_count
                stock_asset.save()
        
        elif sender == SellStockHistory:
            total_cost = instance.stock_value_amount * instance.stock_sold_count 
            cash_assets = CashAssets.objects.get(user = instance.user)
            cash_assets.cash_amount += total_cost
            cash_assets.save()
            
            # this is necessary because it give stock_asset a value, even though a new entry will never be created
            stock_asset, new_entry = StockAssets.objects.get_or_create(
                user = instance.user,
                ticker = instance.ticker,
                defaults = {
                    'stock_count': -instance.stock_sold_count
                }
            )
            if not new_entry:
                stock_asset.stock_count -= instance.stock_sold_count
                stock_asset.save()
            
            

    