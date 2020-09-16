from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Product(models.Model):
    owner_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    item_name = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    description = models.TextField(max_length=64)
    link = models.CharField(max_length=64, default=None, blank=True, null=True)
    time = models.CharField(max_length=64)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.id} {self.item_name}"

    
class Bids(models.Model):
    user_name = models.CharField(max_length=64)
    title_name = models.CharField(max_length=64)
    listing_ID = models.IntegerField()
    bid = models.IntegerField()
    

class Comments():
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments_by_user")
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    product_name = models.ManyToManyField(Product, blank=True, related_name="Comments_on_product")

class Watch_list(models.Model):
    user_name = models.ManyToManyField(User, blank=True, related_name="user_name")
    product_name = models.ManyToManyField(Product, blank=True, related_name="Watch_List")
    
    

class Close_Bid(models.Model):
    owner_name = models.CharField(max_length=64)
    winner_name = models.CharField(max_length=64)
    listing_ID = models.IntegerField()
    win_price = models.IntegerField()


class All_Listing(models.Model):
    listing_ID = models.IntegerField()
    title_name = models.CharField(max_length=64)
    description = models.TextField()
    link = models.CharField(max_length=64, default=None, blank=True, null=True)

