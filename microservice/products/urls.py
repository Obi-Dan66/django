# from django.urls import path
# from products.views import ProductList, ProductDetail, product_offers
# from products import views

# app_name = 'products'

# urlpatterns = [
#     path('products/', ProductList.as_view(), name='product-list'),
#     path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
#     path('products/<int:pk>/offers/', views.product_offers, name='product-offers'),
# ]
from django.urls import path, include
from rest_framework import routers
from products import views
from products.views import ProductList, ProductDetail, product_offers

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
app_name = 'products'

urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<int:pk>/offers/', views.product_offers, name='product-offers'),
]
