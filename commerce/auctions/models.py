from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    owner_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    item_name = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    description = models.TextField(max_length=64)
    link = models.CharField(max_length=64, default=None, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.id} {self.item_name}"

    
class Bids(models.Model):
    user_name = models.OneToOneField(User, blank=True, on_delete=models.CASCADE, related_name="Bid_by")
    title_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="Bid_on_product")
    listing_ID = models.IntegerField()
    bid = models.IntegerField()
    

class Comment():
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments_by_user")
    time = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    product_name = models.ManyToManyField(Product, blank=True, related_name="Comments_on_product")

class Watch_list(models.Model):
    user_ID = models.IntegerField()
    product_ID = models.IntegerField()
    
    




class All_Listing(models.Model):
    listing_ID = models.IntegerField()
    title_name = models.CharField(max_length=64)
    description = models.TextField()
    link = models.CharField(max_length=64, default=None, blank=True, null=True)

