from django.urls import path
from products.views import ProductList, ProductDetail, product_offers

app_name = 'products'

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<int:pk>/offers/', product_offers, name='product-offers'),
]