from decimal import Decimal

from pydantic import BaseModel


class MarketplaceListing(BaseModel):
    title: str
    price: Decimal
    currency: str
    listing_id: str
    listing_url: str
    seller_country: str
    media_condition: str
    sleeve_condition: str
    seller_rating: Decimal