from django.db import models
from django.contrib.postgres.fields import JSONField

from vendor_profile_management.models import Vendor

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    created_Date = models.DateTimeField(auto_now_add=True)
    updated_Date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.po_number

    class Meta:
        db_table = "purchase_orders"