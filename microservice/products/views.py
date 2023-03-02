import requests
import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from microservice.settings import OFFERS_MS_URL
from dotenv import load_dotenv
from products.models import Product, Offer
from products.serializers import ProductSerializer, OfferSerializer
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

class ProductList(APIView):
    """
    List all products, or create a new product.
    """
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # register product to offer service
            register_product(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    """
    Retrieve, update or delete a product instance.
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def product_offers(request, pk):
    """
    Retrieve all offers for a specific product.
    """
    product = Product.objects.get(pk=pk)
    offers = product.offers.all()
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)


def register_product(product_data):
    """
    Register a product to the offer service.
    """
    url = f"{OFFERS_MS_URL}/products/register"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {
        "id": product_data["id"],
        "name": product_data["name"],
        "description": product_data["description"]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == status.HTTP_201_CREATED:
        print("Product registered successfully.")
    else:
        print(f"Failed to register product: {response.json()}")