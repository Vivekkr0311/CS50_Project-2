from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms

from .models import *

class Add_product_Form(forms.Form):
    product_name = forms.CharField(max_length=64)
    product_description = forms.CharField(widget=forms.Textarea, required=False)
    category = forms.CharField(max_length=64)
    link = forms.URLField(required=False)
    price = forms.IntegerField()

def index(request):
    items = []
    if request.user.username: #If user is logged in.
        user = User.objects.get(username=request.user.username)
        items = Product.objects.exclude(owner_name=user).all()
    else: #if user is not logged in.
        items = Product.objects.all()
   
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


    
    
@login_required
def my_products(request, username):
    id = User.objects.get(username=username).pk
    user = User.objects.get(pk=id)
    list_of_product = user.products.all()
    
    return render(request, "auctions/my_product.html", {
        "list_of_product":list_of_product
    })

@login_required
def add_watchlist(request, product_ID):
    pass

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html")

@login_required
def create_listing(request, username):
    if request.method == "POST":
        form = Add_product_Form(request.POST)
        user = User.objects.get(username=username)
        if form.is_valid():
            product_name = form.cleaned_data["product_name"]
            product_description = form.cleaned_data["product_description"]
            category = form.cleaned_data["category"]
            link = form.cleaned_data["link"]
            Bid = form.cleaned_data["price"]

            p = Product(owner_name=user, item_name=product_name, category=category, description=product_description, link=link, price=Bid)
            p.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/create_listing.html", {
                "username":username,
                "form": Add_product_Form()
            })

    return render(request, "auctions/create_listing.html", {
        "username":username,
        "form": Add_product_Form()
    })


@login_required
def your_winnings(request):
    return render(request, "auctions/your_winnings.html")
