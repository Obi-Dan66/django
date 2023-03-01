from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from products.models import Product, Offer
from products.serializers import ProductSerializer, OfferSerializer
from django.conf import settings


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['GET'])
def get_product_offers(request, pk):
    product = Product.objects.get(pk=pk)
    token = request.query_params.get('token')
    url = f'{settings.OFFERS_MS_URL}/products/{product.id}/offers'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        serializer = OfferSerializer(data=response.json(), many=True)
        serializer.is_valid()
        return