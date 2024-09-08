# signals.py
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PurchaseOrder
from vendor_profile_management.models import HistoricalPerformance

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    try:
        vendor = instance.vendor
        
        # Calculate On-Time Delivery Rate
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        if completed_orders.exists():
            on_time_orders = completed_orders.filter(delivery_date__gte=F('delivery_date'))
            vendor.on_time_delivery_rate = (on_time_orders.count() / completed_orders.count()) * 100

        # Calculate Quality Rating Average
        quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        if quality_ratings:
            vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings)

        # Calculate Average Response Time
        response_times = completed_orders.exclude(acknowledgment_date__isnull=True).values_list('issue_date', 'acknowledgment_date')
        total_response_time = sum([(ack_date - issue_date).total_seconds() for issue_date, ack_date in response_times])
        if response_times:
            vendor.average_response_time = total_response_time / len(response_times)

        # Calculate Fulfillment Rate
        fulfilled_orders = completed_orders.filter(status='completed')
        if completed_orders.exists():
            vendor.fulfillment_rate = (fulfilled_orders.count() / completed_orders.count()) * 100
            
            
    # Create a new HistoricalPerformance instance
        HistoricalPerformance(
            vendor=vendor,
            on_time_delivery_rate=vendor.on_time_delivery_rate,
            quality_rating_avg=vendor.quality_rating_avg,
            average_response_time=vendor.average_response_time,
            fulfillment_rate= vendor.fulfillment_rate
        )
        
        vendor.save()

    except Exception as ex:
        print(str(ex))