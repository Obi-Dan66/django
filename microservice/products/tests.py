from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from products.models import Product, Offer
from products.serializers import ProductSerializer, OfferSerializer


class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {'name': 'Test Product', 'description': 'Test Description'}
        self.response = self.client.post(
            reverse('products:product-list'),
            self.product_data,
            format='json')

    def test_create_product(self):
        # Create a Product instance
        product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
        )
    # Make a POST request to create a new product
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'description': 'This is a new product',
            'price': 19.99,
            'quantity': 5
        }
        response = self.client.post(url, data)
    # Check that the response has a 201 status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # Check that the response data matches the data we posted
        self.assertEqual(response.data['name'], 'New Product')
        self.assertEqual(response.data['description'], 'This is a new product')
        self.assertEqual(response.data['price'], '19.99')
        self.assertEqual(response.data['quantity'], 5)

    # def test_get_product_list(self):
    #     response = self.client.get(reverse('products:product-list'))
    #     products = Product.objects.all()
    #     serializer = ProductSerializer(products, many=True)
    #     self.assertEqual(response.data, serializer.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_product_detail(self):
    #     product = Product.objects.get()
    #     response = self.client.get(reverse('products:product-detail', kwargs={'pk': product.id}))
    #     serializer = ProductSerializer(product)
    #     self.assertEqual(response.data, serializer.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_product(self):
    #     product = Product.objects.get()
    #     updated_product = {'name': 'Updated Product', 'description': 'Updated Description'}
    #     response = self.client.put(
    #         reverse('products:product-detail', kwargs={'pk': product.id}),
    #         updated_product,
    #         format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     product.refresh_from_db()
    #     self.assertEqual(product.name, 'Updated Product')
    #     self.assertEqual(product.description, 'Updated Description')

    # def test_delete_product(self):
    #     product = Product.objects.get()
    #     response = self.client.delete(reverse('products:product-detail', kwargs={'pk': product.id}))
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Product.objects.count(), 0)

    # def test_create_offer(self):
    #     product = Product.objects.get()
    #     offer_data = {'price': 9.99, 'currency': 'USD', 'product': product.id}
    #     response = self.client.post(
    #         reverse('offers:offer-list'),
    #         offer_data,
    #         format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Offer.objects.count(), 1)
    #     self.assertEqual(Offer.objects.get().price, 9.99)

    # def test_get_product_offers(self):
    #     product = Product.objects.get()
    #     offer = Offer.objects.create(price=9.99, currency='USD', product=product)
    #     response = self.client.get(reverse('products:product-offers', kwargs={'pk': product.id}))
    #     serializer = OfferSerializer(offer)
    #     self.assertEqual(response.data, serializer.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)