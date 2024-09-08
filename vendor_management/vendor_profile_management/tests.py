import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Vendor

class VendorViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create(
            name='Vendor 1',
            email="vendor1@example.com",
            contact_details='vendor1@example.com',
            address='123 Main St',
            vendor_code='V001'
        )
        self.client.force_authenticate(self.vendor1)

    def test_get_all_vendors(self):
        response = self.client.get(reverse('vendor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       

    def test_get_valid_vendor(self):
        response = self.client.get(reverse('vendor-detail', kwargs={'vendor_id': self.vendor1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Vendor 1')

    def test_get_invalid_vendor(self):
        response = self.client.get(reverse('vendor-detail', kwargs={'vendor_id': 100}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid_vendor(self):
        data = {
            'name': 'New Vendor',
            "password":"vendor126",
            'email': 'newvendor@example.com',
            'contact_details': 'newvendor@example.com',
            'address': '789 Oak St',
            'vendor_code': 'V003'
        }
        response = self.client.post(reverse('register-vendor'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

    def test_create_invalid_vendor(self):
        data = {
            'name': '',
            'contact_details': 'newvendor@example.com',
            'address': '789 Oak St',
            'vendor_code': 'V003'
        }
        response = self.client.post(reverse('register-vendor'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_vendor(self):
        data = {
            'name': 'Updated Vendor 1',
            'contact_details': 'vendor1@example.com',
            'address': '123 Main St',
            'vendor_code': 'V001'
        }
        response = self.client.patch(reverse('update-vendor', kwargs={'vendor_id': self.vendor1.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.get(pk=self.vendor1.pk).name, 'Updated Vendor 1')

    def test_update_invalid_vendor(self):
        data = {
            'name': '',
            'contact_details': 'vendor1@example.com',
            'address': '123 Main St',
            'vendor_code': 'V001'
        }
        response = self.client.patch(reverse('update-vendor', kwargs={'vendor_id': self.vendor1.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_vendor(self):
        response = self.client.delete(reverse('delete-vendor', kwargs={'vendor_id': self.vendor1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_delete_invalid_vendor(self):
        response = self.client.delete(reverse('delete-vendor', kwargs={'vendor_id': 100}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_vendor_performance(self):
        response = self.client.get(reverse('vendor-performance', kwargs={'vendor_id': self.vendor1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('on_time_delivery_rate', response.data.get('data'))
        self.assertIn('quality_rating_avg', response.data.get('data'))
        self.assertIn('average_response_time', response.data.get('data'))
        self.assertIn('fulfillment_rate', response.data.get('data'))