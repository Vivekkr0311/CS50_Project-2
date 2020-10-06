from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages

from .models import *

class Add_product_Form(forms.Form):
    product_name = forms.CharField(max_length=64)
    product_description = forms.CharField(widget=forms.Textarea, required=False)
    category = forms.CharField(max_length=64)
    link = forms.CharField(required=False)
    price = forms.IntegerField()

class Change_Bid_Form(forms.Form):
    new_Bid = forms.IntegerField()


class Comment(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

class Bid_Form(forms.Form):
    Bid = forms.IntegerField()
    
    

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


def item_details(request, item_id):
    item = Product.objects.get(pk=item_id)
    all_comments = Comment_Table.objects.filter(product=item_id)
    all_bids = Bid.objects.filter(on_product=item)
    if request.method == "POST":
        comment = Comment(request.POST)
        if comment.is_valid():
            comment = comment.cleaned_data["comment"]

            user = request.user.username
            u_ID = User.objects.get(username=user)
            p_ID = Product.objects.get(pk=item_id)
            c = Comment_Table(person=u_ID, product=p_ID, comment=comment)
            c.save()

            return render(request, "auctions/item_details.html", {
                "item":item,
                "comment":Comment(),
                "list_of_comments":all_comments,
                "all_bids":all_bids
            })
        #else:
        #   return HttpResponse("Comment is not valid.")

    return render(request, "auctions/item_details.html", {
        "item":item,
        "comment":Comment(),
        "list_of_comments":all_comments,
        "all_bids":all_bids
    })

def show_categories(request):
    products = Product.objects.all()
    categories = []
    for product in products:
        if product.category not in categories:
            categories.append(product.category)
        else:
            continue

    
    return render(request, "auctions/category.html", {
        "categories":categories
    })

def category_search(request):
    category = request.POST["category"]
    
    items = Product.objects.filter(category=category)

    return render(request, "auctions/category_search.html", {
        "items":items
    })

@login_required
def Bid_Now(request, product_id):
    product_object = Product.objects.get(pk=product_id)
    user_object = User.objects.get(username=request.user.username)
    if request.method == "POST":
        bid_raw_data = Bid_Form(request.POST)
        if bid_raw_data.is_valid():
            bid = bid_raw_data.cleaned_data["Bid"]

            p = Product.objects.get(pk=product_id)
            if bid >= p.price:
                Bid_object = Bid(Bid=bid, bid_by=user_object, on_product=product_object)
                Bid_object.save()

                return redirect("index")
            else:
                return render(request, "auctions/Biding.html", {
                    "form":Bid_Form(),
                    "product":product_object,
                    "message":"To win this item, bid with more amount."
                })
    else:
        return render(request, "auctions/Biding.html", {
            "form":Bid_Form(),
            "product":product_object
        })




    return render(request, "auctions/Biding.html", {
        "form":Bid_Form()
    })

@login_required
def delete_bid(request, item_id):

    try:
        p = Product.objects.get(pk=item_id)
        w = Watch_list.objects.get(p_ID=item_id)
        p.delete()
        w.delete()
    except:
        p = Product.objects.get(pk=item_id)
        p.delete()
        return redirect("my_products", request.user.username)

    return redirect("my_products", request.user.username)

@login_required
def close_bid(request, item_id):
    p = Product.objects.get(pk=item_id)
    watchlist_object = Watch_list.objects.filter(p_ID=item_id)
    for each_object in watchlist_object:
        each_object.delete()
    '''try:
        bid_object = Bid.objects.filter(on_product=p)
        return render(request, "auctions/bid_closing_page.html", {
            "all_bids_on_item":bid_object
        })
    except Bid.DoesNotExist:
        return HttpResponse("No winner for your item.")'''
    bid_object = Bid.objects.filter(on_product=p)
    max_bid = max(single_object.Bid for single_object in bid_object)


    #Getting winner's user object and product object.
    bid_object_2 = Bid.objects.get(Bid=max_bid)
    user_object = User.objects.get(username=bid_object_2.bid_by)
    product_won = Product.objects.get(pk=item_id)
    

    #Copying all data to won.
    won_product = All_Won()
    won_product.owner_name = product_won.owner_name
    won_product.item_name = product_won.item_name
    won_product.category = product_won.category
    won_product.description = product_won.description
    won_product.link = product_won.link
    won_product.time = product_won.time

    won_product.save()

    winner = Winner(won_by=user_object, product_won=won_product, on_price=max_bid)
    winner.save()

    #Deleting from all listing.
    product_won.delete()
    

    return render(request, "auctions/bid_closing_page.html", {
        "user":user_object,
        "winner_bid":max_bid,
        "won_product":won_product,
        "all_bids_on_item":bid_object
    })

@login_required
def closed_products(request):
    user = request.user.username
    
    products_were = All_Won.objects.filter(owner_name=user)


    return render(request, "auctions/winner_page.html", {
        "items":products_were
    })

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
    if request.user.username:
        user = User.objects.get(username=request.user.username)
        user_ID = user.pk
        try:
            w = Watch_list.objects.get(u_ID=user_ID, p_ID=product_ID)
            return redirect("watchlist", user_ID)
        except:
            w = Watch_list(u_ID = user_ID, p_ID = product_ID)
            w.save()
            return redirect("watchlist", user_ID)

    
@login_required
def remove_from_watchlist(request, product_ID):
    if request.user.username:
        user = User.objects.get(username=request.user.username)
        user_id = user.pk

        w = Watch_list.objects.get(u_ID=user_id, p_ID=product_ID)
        w.delete()
        return redirect("watchlist", user_id)

@login_required
def watchlist(request, user_id):
    user_ID = user_id

    items = Watch_list.objects.filter(u_ID=user_ID)
    product_IDs = []
    for item in items:
        product_IDs.append(item.p_ID)

    items = []
    for product_id in product_IDs:
        items.append(Product.objects.get(pk=product_id))
    
    return render(request, "auctions/watchlist.html", {
        "user_id":user_ID,
        "items":items
    })

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
            return render(request, "auctions/create_listing.html", {
                "username":username,
                "form": Add_product_Form()
            })

    return render(request, "auctions/create_listing.html", {
        "username":username,
        "form": Add_product_Form()
    })

@login_required
def change_Bid(request, product_ID):

    
    p = Product.objects.get(pk=product_ID)

    if request.method == "POST":
        form = Change_Bid_Form(request.POST)
        user = request.user.username

        if form.is_valid():
            new_Bid = form.cleaned_data["new_Bid"]
            if new_Bid > p.price:

                p.price = new_Bid
                p.save()
                return redirect("my_products", user)
            else:
                messages.warning(request, 'New Bid must be greater than the previous Bid.') 
        else:
            return render(request, "auctions/change_Bid.html", {
                "form":Change_Bid_Form(),
                "product":p
            })
    return render(request, "auctions/change_Bid.html", {
        "form":Change_Bid_Form(),
        "product":p
    })


@login_required
def your_winnings(request):
    user = User.objects.get(username=request.user.username)
    
    winner_objects = Winner.objects.filter(won_by=user)
    
    items_won = []
    for each_object in winner_objects:
        items_won.append(each_object.product_won)
    
    #won_product = winner_object.product_won.item_name
    #on_price = winner_object.on_price
    return render(request, "auctions/your_winnings.html",{
        "items":items_won
        #"on_product":on_product,
        #"item":item
    })
    
