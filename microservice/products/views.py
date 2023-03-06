# import requests
# import os
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.http import Http404
# from microservice.settings import OFFERS_MS_URL
# from dotenv import load_dotenv
# from products.models import Product, Offer
# from products.serializers import ProductSerializer, OfferSerializer
# from django.shortcuts import render
# from django.views import View
# load_dotenv()
# ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# class ProductList(APIView):
#     """
#     List all products, or create a new product.
#     """
#     def get(self, request, format=None):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # register product to offer service
#             register_product(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductDetail(APIView):
#     """
#     Retrieve, update or delete a product instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         product = self.get_object(pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def product_offers(request, pk):
#     """
#     Retrieve all offers for a specific product.
#     """
#     product = Product.objects.get(pk=pk)
#     offers = product.offers.all()
#     serializer = OfferSerializer(offers, many=True)
#     return Response(serializer.data)

# class ProductOffersView(View):
#     def get(self, request, pk):
#         product = Product.objects.get(pk=pk)
#         offers = Offer.objects.filter(product=product)
#         return render(request, 'products/offers.html', {'product': product, 'offers': offers})

# product_offers = ProductOffersView.as_view()

# def register_product(product_data):
#     """
#     Register a product to the offer service.
#     """
#     url = f"{OFFERS_MS_URL}/products/register"
#     headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
#     data = {
#         "id": product_data["id"],
#         "name": product_data["name"],
#         "description": product_data["description"]
#     }
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == status.HTTP_201_CREATED:
#         print("Product registered successfully.")
#     else:
#         print(f"Failed to register product: {response.json()}")
        
# @api_view(['POST'])
# def create_product(request):
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from products.models import Product, Offer
from products.serializers import ProductSerializer, OfferSerializer
from microservice.settings import OFFERS_MS_URL
import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'])
    def offers(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        access_token = get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        url = os.environ.get('OFFERS_MS_URL', 'https://applifting-python-excercise-ms.herokuapp.com/api/v1')
        response = requests.get(f'{url}/products/{product.id}/offers', headers=headers)

        if response.status_code == status.HTTP_200_OK:
            offers = response.json()
            serializer = OfferSerializer(data=offers, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
        else:
            return Response(response.json(), status=response.status_code)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        product = response.data
        access_token = get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        url = os.environ.get('OFFERS_MS_URL', 'https://applifting-python-excercise-ms.herokuapp.com/api/v1')
        data = {'id': product['id'], 'name': product['name'], 'description': product['description']}
        response = requests.post(f'{url}/products/register', headers=headers, json=data)

        if response.status_code != status.HTTP_201_CREATED:
            self.perform_destroy(product['id'])
            return Response(response.json(), status=response.status_code)

        return response

    def perform_destroy(self, instance):
        access_token = get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        url = os.environ.get('OFFERS_MS_URL', 'https://applifting-python-excercise-ms.herokuapp.com/api/v1')
        response = requests.delete(f'{url}/products/{instance.id}/offers', headers=headers)

        if response.status_code != status.HTTP_204_NO_CONTENT:
            return Response(response.json(), status=response.status_code)

        super().perform_destroy(instance)

def get_access_token():
    if hasattr(get_access_token, 'access_token'):
        return get_access_token.access_token

    url = os.environ.get('OFFERS_MS_URL', 'https://applifting-python-excercise-ms.herokuapp.com/api/v1')
    response = requests.post(f'{url}/auth')
    response.raise_for_status()
    access_token = response.json().get('access_token')
    get_access_token.access_token = access_token
    return access_token


def update_offers():
    while True:
        time.sleep(60)
        access_token = get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        url = os.environ.get('OFFERS_MS_URL', 'https://applifting-python-excercise-ms.herokuapp.com/api/v1')
        products = Product.objects.all()

        for product in products:
            response = requests.get(f'{url}/products/{product.id}/offers', headers=headers)
            if response.status_code == status.HTTP_200_OK:
                offers = response.json()
                Offer.objects.filter(product=product).delete()
                for offer in offers:
                    offer['product'] = product
                serializer = OfferSerializer
                
class OfferServiceAuthView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class ProductOfferViewSet(viewsets.ViewSet):
    def list(self, request, pk=None):
        queryset = Offer.objects.filter(product__pk=pk)
        serializer = OfferSerializer(queryset, many=True)
        return Response(serializer.data)