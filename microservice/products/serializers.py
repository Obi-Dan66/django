# from rest_framework import serializers
# from products.models import Product, Offer


# class OfferSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Offer
#         fields = '__all__'


# class ProductSerializer(serializers.ModelSerializer):
#     offers = OfferSerializer(many=True, read_only=True)

#     class Meta:
#         model = Product
#         fields = '__all__'
from rest_framework import serializers
from products.models import Product, Offer

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'price', 'items_in_stock']

class ProductSerializer(serializers.ModelSerializer):
    offers = OfferSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'offers']
