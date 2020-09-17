from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

from .models import *


def index(request):
    items = Product.objects.all()
    #try:
     #   watch_list_count  = Watch_list.objects.filter(user=)

    return render(request, "auctions/index.html",{
        "items":items
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def my_products(request, username):
    id = User.objects.get(username=username).pk
    user = User.objects.get(pk=id)
    list_of_product = user.products.all()
    
    return render(request, "auctions/my_product.html", {
        "list_of_product":list_of_product
    })
    

def add_watchlist(request, product_ID):
    if request.user.username:
       w = Watch_list()
       id = User.objects.get(username=request.user.username).pk
       w.user_ID = id
       w.product_ID = product_ID
       w.save()
    return render(request, "auctions/add_watchlist.html")

def watchlist(request):
    return render(request, "auctions/watchlist.html")

def create_listing(request):
    return render(request, "auctions/create_listing.html")

def your_winnings(request):
    return render(request, "auctions/your_winnings.html")