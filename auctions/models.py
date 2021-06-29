from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import uuid


class Bid(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    def __str__(self):
        return f"{self.id}"


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.title}"


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    min_starting_bid = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    pic = models.ImageField(upload_to ='listing_images/', null=True, blank=True)
    pic_url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        null=True
    )
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='winner'
    )
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.title}"

    def save(self, *args, **kwargs):
        if self.pic_url and not self.pic:
            pic_temp = NamedTemporaryFile(delete=True)
            pic_temp.write(urlopen(self.pic_url).read())
            pic_temp.flush()
            self.pic.save(f"image_{self.uuid}.jpg", File(pic_temp))
        super(Listing, self).save(*args, **kwargs)


@receiver(post_delete, sender=Listing)
def submission_delete(sender, instance, **kwargs):
    instance.pic.delete(False)


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    watchlist_listings = models.ManyToManyField(Listing, blank=True, related_name="watchlist_users")
    def __str__(self):
        return f"{self.id}: {self.username}"