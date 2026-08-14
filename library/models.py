from typing import ClassVar

from django.db import models


class User(models.Model):
    display_name = models.CharField(max_length=200)
    country = models.CharField(max_length=2)
    spotify_id = models.CharField(max_length=200, unique=True)
    profile_url = models.URLField()
    profile_image = models.URLField()


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    release_date = models.DateField()
    spotify_id = models.CharField(max_length=200, unique=True)
    artwork = models.URLField()

    def __str__(self):
        return f"{self.artist} - {self.title}"

class DiscogsMarketplaceListing(models.Model):
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name="discogs_marketplace_listings"
    )
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    listing_id = models.CharField(max_length=200, unique=True)
    listing_url = models.URLField()
    seller_country = models.CharField(max_length=2)
    media_condition = models.CharField(max_length=200)
    sleeve_condition = models.CharField(max_length=200)
    seller_rating = models.DecimalField(max_digits=5, decimal_places=2)


class Match(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="matches")
    listing = models.ForeignKey(
        DiscogsMarketplaceListing, on_delete=models.CASCADE, related_name="matches"
    )
    match_score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["album", "listing"],
                name="unique_album_listing_match"
            )
        ]