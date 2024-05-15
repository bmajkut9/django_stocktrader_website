from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BuyStockHistory, StockAssets

@receiver(post_save, sender=BuyStockHistory)
def update_stock_assets(sender, instance, created, **kwargs):
    if created:
        stock_asset, created = StockAssets.objects.get_or_create(
            user = instance.user,
            ticker = instance.ticker,
            default = {
                'stock_amount': instance.amount,
                'stock_count': instance.count
            }
        )
        if not created:
            stock_asset.stock_amount += instance.amount
            stock_asset.stock_count += instance.count
            stock_asset.save()
    