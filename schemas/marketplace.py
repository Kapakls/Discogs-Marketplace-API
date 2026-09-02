from decimal import Decimal

from pydantic import BaseModel


class MarketplaceListing(BaseModel):
    """Represents a physical release on the Discogs Marketplace."""

    title: str
    price: Decimal
    currency: str
    listing_id: str
    listing_url: str
    seller_country: str
    media_condition: str
    sleeve_condition: str
    seller_rating: Decimal  
    similarity: float = 0.0


class MarketplaceMatchResponse(BaseModel):
    """Contains the marketplace listings matching an album search."""

    album: str
    threshold: float
    total: int
    listings: list[MarketplaceListing]


class AlbumMatchRequest(BaseModel):
    """Represents a request to find marketplace listings for an album."""

    artist: str
    album: str


class BatchMatchRequest(BaseModel):
    """Represents a request to find marketplace listings for multiple albums."""

    albums: list[AlbumMatchRequest]
    threshold: float = 0.1