from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BuyStockHistory, StockAssets, SellStockHistory


@receiver(post_save, sender=BuyStockHistory)
@receiver(post_save, sender=SellStockHistory)
def update_stock_assets(sender, instance, created, **kwargs):
    if created:
        if sender == BuyStockHistory:
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
            stock_asset, new_entry = StockAssets.objects.get_or_create(
                user = instance.user,
                ticker = instance.ticker,
                defaults = {
                    'stock_value_amount': -instance.stock_value_amount,
                    'stock_count': -instance.stock_sold_count
                }
            )
            if not new_entry:
                stock_asset.stock_value_amount -= instance.stock_value_amount
                stock_asset.stock_count -= instance.stock_sold_count
                stock_asset.save()
            
            

    