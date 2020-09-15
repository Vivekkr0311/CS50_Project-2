from django.contrib import admin
from .models import *
# Register your models here.
class User_Admin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
class active_list_Admin(admin.ModelAdmin):
    list_display = ("id", "item_name", "owner_name", "category", "price", "time", "description", "link")

admin.site.register(User, User_Admin)
admin.site.register(Active_listing, active_list_Admin)
