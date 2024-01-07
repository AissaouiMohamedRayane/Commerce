from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

from django.contrib.auth.models import User


def index(request):
    return render(request, "auctions/index.html",{
        "auctions":Auction.objects.all()
    })


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:index"),)
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
    
    
def create_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('auctions:login'))
    if request.method=="POST":
        user=request.user
        name=request.POST["name"]
        category=Category.objects.get(category=request.POST["category"])
        price=request.POST["price"]
        auction=Auction(user=user, name=name, category=category, price=price)
        auction.save()
        return HttpResponseRedirect(reverse("auctions:index"))
    categories=Category.objects.all()
    categories=categories.order_by('category')
    return render(request, 'auctions/create_listing.html',{
        "category":categories
    })

def bid(request, auction_name, auction_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('auctions:login'))
    auction=Auction.objects.get(pk=auction_id)
    if request.method=="POST":
        my_auction=Auction.objects.filter(user=request.user)
        if auction in my_auction:
            return render(request, 'auctions/auction.html',{
        "auction":auction,
        "message":"You can't bid on your auction"
    })
        bid=request.POST["bid"]
        bid=Bids(user=request.user, auction=auction, bid_price=bid)
        user_bids = Bids.objects.filter(user=request.user, auction=auction)
        if user_bids:
            user_bids.delete()
        bid.save()
        return HttpResponseRedirect(reverse("auctions:index"))
    return render(request, 'auctions/bid.html',{
        "auction_name":auction_name,
        "auction_id":auction_id,
        "auction":auction,
        "existing_bids":Bids.objects.filter(auction=auction)
    }
                  
                  
                  )
def auction(request, auction_name, auction_id):
    auction=Auction.objects.get(pk=auction_id)
    return render(request, 'auctions/auction.html',{
        "auction":auction,
    })