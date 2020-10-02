from django.contrib import admin
from .models import *
# Register your models here.

class User_Admin(admin.ModelAdmin):
    list_display = ("id", "username")

class Product_Admin(admin.ModelAdmin):
    list_display = ("id", "item_name", "owner_name", "price")



class Watch_list_Admin(admin.ModelAdmin):
    list_display = ("id", "u_ID", "p_ID")

class Comment_Table_Admin(admin.ModelAdmin):
    list_display = ("id", "person", "product", "comment", "time")

class Bid_Admin(admin.ModelAdmin):
    list_display = ("id", "Bid", "bid_by", "on_product")

class Winner_Admin(admin.ModelAdmin):
    list_display = ("id", "won_by", "product_won", "on_price")

admin.site.register(User, User_Admin)
admin.site.register(Product, Product_Admin)
admin.site.register(Watch_list, Watch_list_Admin)
admin.site.register(Comment_Table, Comment_Table_Admin)
admin.site.register(Bid, Bid_Admin)
admin.site.register(Winner, Winner_Admin)
admin.site.register(All_Won)
