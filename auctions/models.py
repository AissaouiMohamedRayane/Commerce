from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models

class Category(models.Model):
    category=models.CharField(max_length=50)
    def __str__(self):
        return f"{self.category}"


class Auction(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name='auctions')
    name=models.CharField(max_length=50)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='auctions')
    price=models.FloatField(validators=[MinValueValidator(0.01)])
    image=models.ImageField(upload_to='images/', default="C:/Users/OMEN 16/Desktop/django/commerce/auctions/media/images/test.avif")
    def __str__(self):
        return f"{self.pk} {self.name} ${self.price}"


class Bids(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name='bids')
    auction=models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bid_price=models.FloatField()
    def clean(self):
        if self.auction.price>self.bid_price:
            raise ValidationError("Bid price cannot be lower than the auction price.")
    def __str__(self):
        return f"{self.user.username} ${self.bid_price}"