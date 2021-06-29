from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse,  reverse_lazy

from decimal import Decimal
from datetime import datetime

from .models import Bid, Category, Comment, Listing, User
from .forms import CreateNewListingForm


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_listings(request, category_id):
    listings = Listing.objects.filter(category=category_id, active=True)
    category_name = Category.objects.get(id=category_id)
    return render(request, "auctions/category_listings.html", {
        "name": category_name,
        "listings": listings
    })


@login_required(login_url=reverse_lazy("auctions:login"))
def close_listing(request, listing_id):
    if request.method == "POST":
        # listing
        listing = Listing.objects.get(pk=listing_id)
        listing.closed_at = datetime.now()
        listing.active = False
        try:
            current_bid = listing.bids.latest("amount")
            current_bidder = current_bid.user
            listing.winner = current_bidder
        except Bid.DoesNotExist:
            pass
        listing.save()

        # return to listing page
        return redirect("auctions:listing", listing_id=listing_id)
    # return to listing page
    return redirect("auctions:listing", listing_id=listing_id)


@login_required(login_url=reverse_lazy("auctions:login"))
def comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        title = request.POST["title"]
        comment = request.POST["comment"]
        new_comment = Comment.objects.create(
            listing=listing,
            user=user,
            title=title,
            text=comment
        )
        new_comment.save()
    # return to listing page
    return redirect("auctions:listing", listing_id=listing_id)


@login_required(login_url=reverse_lazy("auctions:login"))
def create_listing(request):
    if request.method == "POST":
        form = CreateNewListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.user = request.user
            new_listing.active = True
            new_listing.save()
        return HttpResponseRedirect(reverse("auctions:index"))
    return render(request, "auctions/create_listing.html", {
        "form": CreateNewListingForm()
    })


def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    try:
        user = request.user
        watchlist = user.watchlist_listings.filter(id=listing_id).exists()
    except AttributeError:
        watchlist = None

    try:
        current_bid = listing.bids.latest("amount")
    except Bid.DoesNotExist:
        current_bid = None

    comments = listing.comments.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_bid": current_bid,
        "comments": comments,
        "watchlist": watchlist
    })


def login_view(request):
    context = {
        "next": request.GET["next"]
        if request.GET and "next" in request.GET
        else reverse("auctions:index")
    }

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        redirect = request.POST["next"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(redirect)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, "auctions/login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


@login_required(login_url=reverse_lazy("auctions:login"))
def place_bid(request, listing_id):
    if request.method == "POST":
        # get user / listing
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        new_bid = Decimal(request.POST["bid"])

        try:
            minimum_acceptable_bid = listing.bids.latest("amount").amount + Decimal(0.01)
        except Bid.DoesNotExist:
            minimum_acceptable_bid = listing.min_starting_bid

        if new_bid >= minimum_acceptable_bid:
            new_bid_entry = Bid.objects.create(
                listing=listing,
                user=user,
                amount=new_bid
            )
            new_bid_entry.save()

        # return to listing page
        return redirect("auctions:listing", listing_id=listing_id)
    # return to listing page
    return redirect("auctions:listing", listing_id=listing_id)


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url=reverse_lazy("auctions:login"))
def watchlist(request):
    user = request.user
    listings = user.watchlist_listings.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required(login_url=reverse_lazy("auctions:login"))
def watchlist_add(request, listing_id):
    if request.method == "POST":
        # get user / listing
        user = request.user
        listing = Listing.objects.get(pk=listing_id)

        # add listing to watchlist
        user.watchlist_listings.add(listing)

        # return to listing page
        return redirect("auctions:listing", listing_id=listing_id)

@login_required(login_url=reverse_lazy("auctions:login"))
def watchlist_remove(request, listing_id):
    if request.method == "POST":
        # get user / listing
        user = request.user
        listing = Listing.objects.get(pk=listing_id)

        # add listing to watchlist
        user.watchlist_listings.remove(listing)

        # return to listing page
        return redirect("auctions:listing", listing_id=listing_id)