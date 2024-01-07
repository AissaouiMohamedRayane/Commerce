from django.urls import path

from . import views

app_name="auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Create/", views.create_listing, name="create_listing"),
    path("<str:auction_name><int:auction_id>/bid", views.bid, name="bid"),
    path("<str:auction_name><int:auction_id>", views.auction, name="auction"),
]
