# from django.db import models

# class Product(models.Model):
#     id = models.CharField(max_length=100, primary_key=True)
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=255)

# class Offer(models.Model):
#     id = models.CharField(max_length=100, primary_key=True)
#     price = models.IntegerField()
#     items_in_stock = models.IntegerField()
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers')
from django.db import models

class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Offer(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    product = models.ForeignKey(Product, related_name='offers', on_delete=models.CASCADE)
    price = models.IntegerField()
    items_in_stock = models.IntegerField()

    def __str__(self):
        return f'{self.product}: {self.price} ({self.items_in_stock} in stock)'
