from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from purchase_orders.models import PurchaseOrder
from vendor_profile_management.models import Vendor
from datetime import datetime
import pytz

class PurchaseOrderViewsTestCase(APITestCase):

    
    def setUp(self):
        self.client = APIClient()
        # Create a naive datetime object
        naive_datetime = datetime(2022, 1, 1)
        # Make the datetime object aware
        aware_datetime = naive_datetime.astimezone(pytz.UTC)
        self.vendor = Vendor.objects.create(name="Test Vendor",email="test@example.com",contact_details="test@example.com", address="123 Test St",vendor_code="1234vend")
        self.client.force_authenticate(user=self.vendor)
        self.purchase_order = PurchaseOrder.objects.create(po_number="PO123", vendor=self.vendor, order_date=aware_datetime, delivery_date=aware_datetime, items={"item1": 10}, quantity=10, status="pending",issue_date=aware_datetime)

    def test_create_purchase_order(self):
        url = reverse('create_order')
        data = {
            "po_number": "PO456",
            "vendor": self.vendor.id,
            "order_date": "2022-01-01",
            "delivery_date": "2022-01-15",
            "items": {"item1": 10},
            "quantity": 10,
            "status": "pending",
            "issue_date":"2022-01-01"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_purchase_orders(self):
        url = reverse('list-purchase-orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_purchase_order(self):
        url = reverse('order-details', kwargs={'po_id': self.purchase_order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_update_purchase_order(self):
        url = reverse('order-details', kwargs={'po_id': self.purchase_order.id})
        data = {
            "po_number": "PO789",
            "vendor": self.vendor.id,
            "order_date": "2022-01-01",
            "delivery_date": "2022-01-15",
            "items": {"item1": 10},
            "quantity": 10,
            "status": "completed"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_purchase_order(self):
        url = reverse('order-details', kwargs={'po_id': self.purchase_order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)