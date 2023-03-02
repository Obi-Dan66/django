from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from products.models import Product

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {'name': 'Test Product', 'description': 'This is a test product.'}
        self.response = self.client.post(
            reverse('products:product-list'),
            self.product_data,
            format='json'
        )

    def test_create_product(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_get_product_list(self):
        response = self.client.get(reverse('products:product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_detail(self):
        response = self.client.get(reverse('products:product-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_update_product(self):
        new_product_data = {'name': 'Updated Test Product', 'description': 'This is an updated test product.'}
        response = self.client.put(reverse('products:product-detail', args=[1]), new_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().name, 'Updated Test Product')

    def test_delete_product(self):
        response = self.client.delete(reverse('products:product-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_get_product_offers(self):
        response = self.client.get(reverse('products:product-offers', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0) # No offers registered yet