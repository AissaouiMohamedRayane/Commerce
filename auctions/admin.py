from django.contrib import admin

from .models import *
class adminBids(admin.ModelAdmin):
    list_display=['user', 'auction', 'bid_price']

admin.site.register(Auction)

admin.site.register(Bids, adminBids)

admin.site.register(Category)

