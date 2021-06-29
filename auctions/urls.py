from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_listings, name="category_listings"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/close_listing", views.close_listing, name="close_listing"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("<int:listing_id>/watchlist_add", views.watchlist_add, name="watchlist_add"),
    path("<int:listing_id>/watchlist_remove", views.watchlist_remove, name="watchlist_remove"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
]
