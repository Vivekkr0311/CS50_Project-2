from django.contrib import admin
from .models import *
# Register your models here.
class User_Admin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
class Product_Admin(admin.ModelAdmin):
    list_display = ("id", "item_name", "owner_name", "category", "price", "time", "description", "link")

class Watch_list_Admin(admin.ModelAdmin):
    list_display = ("user_name", "product_name")

admin.site.register(User, User_Admin)
admin.site.register(Product, Product_Admin)
admin.site.register(Watch_list)
admin.site.register(Comments)