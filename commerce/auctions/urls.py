from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.show_categories, name="categories"),
    path("biding/<int:product_id>", views.Bid_Now, name="bid_now"),
    path("category_search", views.category_search, name="categories_result"),
    path("my_products/<str:username>", views.my_products, name="my_products"),
    path("addwatchlist/<int:product_ID>", views.add_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:product_ID>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("create_listing/<str:username>", views.create_listing, name="create_listing"),
    path("your_winnings/", views.your_winnings, name="your_winnings"),
    path("changeBid/<int:product_ID>", views.change_Bid, name="change_Bid"),
    path("item_details/<int:item_id>", views.item_details, name="item_details"),
    path("delete_bid/<int:item_id>", views.delete_bid, name="delete_bid"),
    path("close_bid/<int:item_id>", views.close_bid, name="close_bid"),
    path("closed_products", views.closed_products, name="closed_products")
    #path("categories", views.categories, name="categories"),
   # path("categories/<str:category>", views.category, name="category"),
   
]
