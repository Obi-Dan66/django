from django.db import models


class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()


class Offer(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    price = models.IntegerField()
    items_in_stock = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers')