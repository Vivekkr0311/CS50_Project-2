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
    description = models.TextField(max_length=64, blank=True)
    link = models.CharField(max_length=64, default=None, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.id} {self.item_name}"
    

class Watch_list(models.Model):
    u_ID = models.IntegerField()
    p_ID = models.IntegerField()


class Comment_Table(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person_in_comments")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_in_comments")
    comment = models.TextField()
    time = models.DateTimeField(default=timezone.now)

class Category(models.Model):
    pass